import hashlib
import json
import math
import queue
import struct
import sys
import time
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from eval_translate import (CONFIGS, ENG, ENGINE, MAX_NEW, QT_NAME, append_jsonl, code_version, footprint_peak_mib,
                            gpu_peak_bytes, load_data, messages, open_dir, pairs, prompt, read_jsonl, sample_ids,
                            sha256)

PACK_TOKENS = 1024                                     # scored tokens per packed forward


def end_of_answer(eng) -> int:
    """The token the chat template writes right after an assistant's answer (one of the model's stops)."""
    from chat import format_chat
    mark = "\ue000"                                  # a private-use character: in no template
    s = format_chat([{"role": "user", "content": "u"}, {"role": "assistant", "content": mark}],
                    add_generation_prompt=False, style=eng.chat_style)
    if not (ids := eng.tokenizer.encode(s[s.index(mark) + 1:])) or ids[0] not in eng.eos_ids:
        sys.exit(f"{eng.name}: the template ends an answer with {ids[:2]}, not one of the stops {sorted(eng.eos_ids)}")
    return ids[0]


def added_tokens(model: str) -> tuple[set[int], set[int]]:
    """A tokenizer's added tokens: those flagged special (skip_special_tokens drops them from an output), and the
    others that are not whitespace (kept, as there: Gemma 3's HTML tags and unused slots)."""
    from engine import MODELS
    spec = json.load(open(ENGINE / MODELS[model]["dir"] / "tokenizer.json", encoding="utf-8"))["added_tokens"]
    return ({t["id"] for t in spec if t["special"]},
            {t["id"] for t in spec if not t["special"] and t["content"].replace("\u2581", " ").strip()})


def qt_header(path) -> tuple[str, dict]:
    """A .qt file's header (every tensor's name, scheme, shape and offsets) and its SHA-256."""
    with open(path, "rb") as f:
        raw = f.read(struct.unpack("<Q", f.read(8))[0])
    return hashlib.sha256(raw).hexdigest(), json.loads(raw)


def weights_identity(config: str, weights: str | None) -> dict:
    """What the config's weights are: the .qt by its header, or quantized at load (with the policy file, if any).
    An INT4 file is calibrated if it keeps a tensor at INT8 beyond those every INT4 file keeps (quant.scheme_for: the
    tied embedding). Refuses a file of another scheme, a calibrated config whose weights are flat, and the reverse."""
    from engine import MODELS
    from quant import scheme_for
    model, backend, policy = CONFIGS[config]
    if weights:
        head_sha, head = qt_header(weights)
        if (scheme := head.pop("__metadata__")["scheme"]) != backend.removeprefix("metal-"):
            sys.exit(f"{weights} is {scheme}, {config} runs {backend}")
        q = {k.split("::")[0]: v["scheme"] for k, v in head.items() if "scheme" in v}
        kept = sum(s == "int8" and scheme_for(n, "int4") == "int4" for n, s in q.items())
        w = dict(file=Path(weights).name, bytes=Path(weights).stat().st_size, header_sha256=head_sha,
                 schemes=Counter(q.values()), policy_int8=kept if scheme == "int4" else None)
        mixed, what = kept > 0, Path(weights).name
    else:
        p = MODELS[model].get("policy") if backend == "metal-int4" else None
        p = p if p and (ENGINE / p).exists() else None
        w = dict(file=None, policy=p, policy_sha256=p and sha256(ENGINE / p))
        mixed, what = p is not None, f"quantizing at load ({p or 'no policy file'})"
    if policy and mixed != (policy == "calibrated"):
        sys.exit(f"{config} needs {policy} INT4 weights, but {what} is {'calibrated' if mixed else 'flat'}: "
                 + (f"write {QT_NAME['flat']} with scripts/quantize.py --scheme int4 and no --policy" if mixed else
                    "write the policy with scripts/calibrate_quant.py and quantize with --policy"))
    return w


def open_run(a, kind: str, manifest: dict):
    """-> (engine, run directory, done_in) for an engine config; its identity: weights, policy, prompts, stops, limits,
    seed, dataset."""
    if not (ENGINE / "src/engine.py").exists():
        sys.exit(f"no engine at {ENGINE}: set ENGINE to the InferenceEngine checkout")
    from engine import MODELS, load_engine
    model, backend, policy = CONFIGS[a.config]
    qt = ENGINE / MODELS[model]["dir"] / QT_NAME[policy]
    weights = a.weights or (str(qt) if backend.startswith("metal-int") and qt.exists() else None)
    w = weights_identity(a.config, weights)                       # before loading: a refusal costs nothing
    eng = load_engine(model, backend, weights)
    style = a.prompt or "card"
    identity = json.loads(json.dumps(dict(
        config=a.config, model=model, backend=backend, weights=w, eos=sorted(eng.eos_ids),
        end_of_answer=end_of_answer(eng), max_new=MAX_NEW, prompt=style,
        messages=messages(style, "{Source}", "{Target}", "{text}"),
        example_prompt=prompt(eng, ENG, "mni", "{text}", style), seed=a.seed, dataset=manifest["jsonl_sha256"])))
    return eng, *open_dir(a, kind, identity)


def run_batched(eng, jobs: list, batch: int, kv_blocks: int, prefix_cache: bool, on_done) -> dict:
    """jobs [(key, prompt ids, max_new)] through the server's scheduler, `batch` in flight; on_done(key, ids, finish,
    ttft) as each finishes. -> the scheduler's facts (preemptions, prefix cache)."""
    from sampler import SamplingParams
    from server.metrics import Metrics
    from server.scheduler import Scheduler
    metrics, events = Metrics(), queue.Queue()
    sched = Scheduler(eng, metrics, max_batch=batch, max_waiting=batch + 1, kv_blocks=kv_blocks,
                      max_model_len=eng.max_model_len or 8192, prefix_cache=prefix_cache)
    greedy, pending, live = SamplingParams(temperature=0.0, top_k=1, top_p=1.0), iter(jobs), {}

    def submit_next() -> None:
        if (job := next(pending, None)) is not None:     # its channel tags events with the job's key
            out = SimpleNamespace(put=lambda ev, key=job[0]: events.put((key, ev)))
            live[job[0]] = sched.submit(job[1], greedy, job[2], out=out)
    try:
        for _ in range(batch):
            submit_next()
        while live:
            key, (kind, payload) = events.get()
            if kind == "token":
                continue
            req = live.pop(key)
            if kind == "error":
                raise RuntimeError(f"{key}: {payload}")
            on_done(key, req.generated, req.finish_reason,
                    req.first_token_at - req.arrived if req.first_token_at is not None else None)
            submit_next()
    finally:
        sched.shutdown(drain_timeout=0)
    return dict(preempted=metrics.counters["requests_preempted_total"], prefix_cache=sched.prefix_note)


def generate(a) -> None:
    items, manifest = load_data(a.data)
    eng, run, done_in = open_run(a, "gen", manifest)
    tok, cap, jobs = eng.tokenizer, eng.max_model_len or 8192, []
    special, added = added_tokens(eng.name)
    for src, tgt, path, todo in pairs(items, sample_ids(items, a.n, a.seed), a.langs, done_in):
        for i in todo:
            text = items[i]["text"][src]
            ids = tok.encode(prompt(eng, src, tgt, text, a.prompt))
            jobs.append(((path, i), ids, min(MAX_NEW[0] + math.ceil(MAX_NEW[1] * len(text)), cap - len(ids))))
    print(f"{a.config}: {len(jobs)} translations to make", flush=True)
    if not jobs:
        return
    totals, t0 = Counter(), time.perf_counter()

    def on_done(key, out, finish, ttft):
        keep = [t for t in out if t not in special]
        hyp = tok.decode(keep).strip()
        append_jsonl(key[0], dict(id=key[1], hyp=hyp, tokens=len(out), stop=finish, ttft=ttft,
                                  special=len(out) - len(keep), added=sum(t in added for t in keep)))
        totals.update(requests=1, tokens=len(out), chars=len(hyp))
        if totals["requests"] % 50 == 0:
            el = time.perf_counter() - t0
            print(f"  {totals['requests']}/{len(jobs)}  {totals['tokens'] / el:.1f} tok/s  [{el:.0f} s]", flush=True)
    facts = run_batched(eng, jobs, a.batch, a.kv_blocks, not a.no_prefix_cache, on_done)
    secs, gpu = time.perf_counter() - t0, gpu_peak_bytes(eng.model.b.device)
    weights = sum(w.nbytes if hasattr(w, "scheme") else w.numel() * w.element_size()    # as bench.py counts them
                  for w in eng.model._cache.values())
    append_jsonl(run / "speed.jsonl", dict(
        totals, secs=secs, batch=a.batch, kv_blocks=a.kv_blocks, weights_bytes=weights, gpu_peak_bytes=gpu,
        footprint_peak_mib=footprint_peak_mib(), date=time.strftime("%Y-%m-%d %H:%M"), **facts))
    append_jsonl(run / "segments.jsonl", dict(kind="gen", items=len(jobs), date=time.strftime("%Y-%m-%d %H:%M"),
                                              **code_version()))
    print(f"{a.config}: {totals['tokens'] / secs:.1f} tok/s, {totals['chars'] / secs:.0f} chars/s over {secs:.0f} s; "
          f"{facts}", flush=True)


def teacher_forced(model, seqs: list, vocab: int, stops: list[int] | None = None):
    """seqs [(key, prompt ids, continuation ids)] -> yields (key, -ln P(token | prompt, the tokens before it) for each
    continuation token, float64). The prompts' common
    prefix (a chat template's preamble) is prefilled once and forked for each sequence; the rest runs packed."""
    import torch
    from decision import FORK_BUDGET, PREFILL_CHUNK, _boundary_logprobs, _fork_bytes, _token_logprobs
    first = [p for _, p, _ in seqs]
    common = next((i for i, col in enumerate(zip(*first)) if len(set(col)) > 1), len(first[0]))
    common = min(common, min(map(len, first)) - 1)             # each sequence keeps its last prompt token
    base = model.new_state(common + max(len(p) - common + len(c) for _, p, c in seqs))
    for i in range(0, common, PREFILL_CHUNK):
        model.forward(torch.tensor(first[0][i:min(i + PREFILL_CHUNK, common)]), state=base, last_only=True)
    per_pack = max(1, FORK_BUDGET // _fork_bytes(base))

    def run(pack):
        h = model.packed_hidden([(torch.tensor(p[common:] + c[:-1]), base.fork()) for _, p, c in pack])
        rows, off = [], 0
        for _, p, c in pack:                                    # row j predicts the chunk's token j + 1
            rows += range(off + len(p) - common - 1, off + len(p) - common - 1 + len(c))
            off += len(p) - common + len(c) - 1
        hr = h[torch.tensor(rows, device=h.device)]
        lp = _token_logprobs(model, hr, [t for *_, c in pack for t in c], vocab)
        ends = np.cumsum([len(c) for *_, c in pack]).tolist()
        if stops:                                               # the answer ends at any stop, not one chosen id
            last = torch.tensor([e - 1 for e in ends], device=h.device)
            mask = torch.zeros(vocab, dtype=torch.bool, device=h.device)
            mask[torch.tensor(stops, device=h.device)] = True
            lp[last.cpu()] = _boundary_logprobs(model, hr[last], mask, vocab)
        yield from ((key, -lp[e - len(c):e].double().numpy()) for (key, _, c), e in zip(pack, ends))
    pack, n = [], 0
    for s in seqs:
        size = len(s[1]) - common + len(s[2])
        if pack and (len(pack) == per_pack or n + size > PACK_TOKENS):
            yield from run(pack)
            pack, n = [], 0
        pack.append(s)
        n += size
    if pack:
        yield from run(pack)


def score(a) -> None:
    items, manifest = load_data(a.data)
    eng, run, done_in = open_run(a, "score", manifest)
    tok, t0, eoa, made = eng.tokenizer, time.perf_counter(), end_of_answer(eng), 0
    for src, tgt, path, todo in pairs(items, sample_ids(items, a.n, a.seed), a.langs, done_in):
        seqs = [(i, tok.encode(prompt(eng, src, tgt, items[i]["text"][src], a.prompt)),
                 tok.encode(items[i]["text"][tgt]) + [eoa]) for i in todo]
        stops = sorted(eng.eos_ids)
        for (i, p, c), (_, nats) in zip(seqs, teacher_forced(eng.model, seqs, tok.vocab_size(), stops) if seqs else ()):
            ref = items[i]["text"][tgt]
            append_jsonl(path, dict(id=i, prompt_tokens=len(p), ref_tokens=len(c) - 1, nats=float(nats[:-1].sum()),
                                    end_nats=float(nats[-1]), chars=len(ref), roundtrip=tok.decode(c[:-1]) == ref))
        made += len(seqs)
        if seqs:
            rs = read_jsonl(path)
            print(f"{src}-{tgt}: {sum(r['nats'] for r in rs) / math.log(2) / sum(r['chars'] for r in rs):.3f} "
                  f"bits/char ({len(rs)} references) [{time.perf_counter() - t0:.0f} s]", flush=True)
    if made:
        append_jsonl(run / "segments.jsonl", dict(kind="score", items=made, date=time.strftime("%Y-%m-%d %H:%M"),
                                                  **code_version()))
