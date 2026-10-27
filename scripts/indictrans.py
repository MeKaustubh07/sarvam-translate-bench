import gc
import importlib.metadata
import json
import math
import time
from collections import Counter
from contextlib import contextmanager
from pathlib import Path

import numpy as np

from eval_translate import (ENG, MAX_NEW, ROOT, append_jsonl, code_version, footprint_peak_mib, gpu_peak_bytes,
                            import_without_init, load_data, open_dir, pairs, read_jsonl, sample_ids, sha256)

HF = {"indictrans2": {"en-x": "data/models/indictrans2-en-indic-1B", "x-en": "data/models/indictrans2-indic-en-1B"}}
# IndicTrans2's languages, as FLORES-200 codes (its README); IN22-Gen's columns use the same codes
CODES = {"asm_Beng", "ben_Beng", "brx_Deva", "doi_Deva", "eng_Latn", "gom_Deva", "guj_Gujr", "hin_Deva", "kan_Knda",
         "kas_Arab", "kas_Deva", "mai_Deva", "mal_Mlym", "mar_Deva", "mni_Beng", "mni_Mtei", "npi_Deva", "ory_Orya",
         "pan_Guru", "san_Deva", "sat_Olck", "snd_Arab", "snd_Deva", "tam_Taml", "tel_Telu", "urd_Arab"}
LIBS = ("IndicTransToolkit", "indic-nlp-library", "sacremoses")
BPC_TEXT = "IndicProcessor's pre-processed reference"


def flores(code: str, manifest: dict) -> str:
    """Our 639-3 code -> IndicTrans2's tag, in the script IN22-Gen's column (and the prompts) use."""
    tag = f"{code}_{manifest['languages'][code]['script']}"
    if tag not in CODES:
        raise SystemExit(f"{tag}: not an IndicTrans2 language")
    return tag


def processor(inference: bool):
    """IndicTransToolkit's IndicProcessor. Its package __init__ imports a collator that fails on transformers 5, and
    IndicNLP's Urdu normalizer imports urduhack, whose __init__ needs TensorFlow: neither is used, so both packages are
    registered without running their __init__."""
    import_without_init("IndicTransToolkit")
    import_without_init("urduhack")
    from IndicTransToolkit.processor import IndicProcessor
    return IndicProcessor(inference=inference)


class Seq2Seq:
    """One direction's model at a time (English -> X, then X -> English): two 1B models do not share 8 GB."""

    def __init__(self, config: str, device: str, dtype: str):
        self.dirs, self.device, self.dtype = HF[config], device, dtype
        self.side = self.model = self.tok = None

    def load(self, src: str):
        import torch
        import transformers
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        side = "en-x" if src == ENG else "x-en"
        if side != self.side:
            remote = (ROOT / self.dirs[side] / "modeling_indictrans.py").exists()
            if remote and int(transformers.__version__.split(".")[0]) >= 5:
                raise SystemExit(f"IndicTrans2's remote code is written for transformers 4, this is "
                                 f"{transformers.__version__}: run it with .venv-it2/bin/python (README)")
            self.model = self.tok = None
            gc.collect()
            if self.device == "mps":
                torch.mps.empty_cache()
            d = ROOT / self.dirs[side]
            self.tok = AutoTokenizer.from_pretrained(d, trust_remote_code=True)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(d, trust_remote_code=True, dtype=getattr(
                torch, self.dtype)).to(self.device).eval()
            self.side = side
        return self.model, self.tok

    def identity(self) -> dict:
        def one(name: str) -> dict:
            d = ROOT / name
            meta = d / ".cache/huggingface/download/config.json.metadata"   # hf download --local-dir: commit first
            w = d / "model.safetensors"
            return dict(dir=name, revision=meta.read_text().split()[0] if meta.exists() else None,
                        config_sha256=sha256(d / "config.json"), weights_bytes=w.stat().st_size if w.exists() else None)
        return {side: one(d) for side, d in self.dirs.items()}


def identity(a, s: Seq2Seq, manifest: dict) -> dict:
    if a.prompt or a.weights:
        raise SystemExit(f"{a.config}: --prompt and --weights are engine options")
    ip = processor(True)
    return json.loads(json.dumps(dict(
        config=a.config, model=a.config, backend="hf", weights=s.identity(), device=a.device, dtype=a.dtype,
        decoding="greedy (num_beams=1), KV cache", max_new=MAX_NEW, prompt="none: IndicProcessor's language tags",
        messages=None, example_prompt=ip.preprocess_batch(["TEXT"], src_lang="eng_Latn", tgt_lang="mni_Mtei")[0],
        processor={k: importlib.metadata.version(k) for k in LIBS}, bpc_text=BPC_TEXT, seed=a.seed,
        dataset=manifest["jsonl_sha256"])))


def encode(tok, texts: list[str], device):
    return tok(texts, padding="longest", truncation=True, return_tensors="pt", return_attention_mask=True).to(device)


@contextmanager
def no_grad():
    import torch
    with torch.no_grad():
        yield


@no_grad()
def greedy(model, tok, src: list[str], max_new: list[int], device) -> tuple[list[list[int]], list[str], float]:
    """Greedy decoding of a batch with the KV cache (the model's own forward, not transformers' generate). ->
    (each output's tokens without the end token, "stop" | "length", seconds to the first token). Rows that finished
    are fed padding; batch rows do not interact."""
    import torch
    t0, cfg = time.perf_counter(), model.config
    enc_in = encode(tok, src, device)
    enc = model.get_encoder()(input_ids=enc_in["input_ids"], attention_mask=enc_in["attention_mask"])
    cur = torch.full((len(src), 1), cfg.decoder_start_token_id, device=device)
    out, stop, past, first = [[] for _ in src], [None] * len(src), None, None
    for _ in range(max(max_new)):
        o = model(encoder_outputs=enc, attention_mask=enc_in["attention_mask"], decoder_input_ids=cur,
                  past_key_values=past, use_cache=True)
        past, nxt = o.past_key_values, o.logits[:, -1].argmax(-1).tolist()
        first = first or time.perf_counter() - t0
        for b, t in enumerate(nxt):
            if stop[b] is None:
                if t == cfg.eos_token_id:
                    stop[b] = "stop"
                else:
                    out[b].append(t)
                    stop[b] = "length" if len(out[b]) == max_new[b] else None
        if all(stop):
            break
        cur = torch.tensor([[t if s is None else cfg.pad_token_id] for t, s in zip(nxt, stop)], device=device)
    return out, stop, first


def generate(a) -> None:
    items, manifest = load_data(a.data)
    s = Seq2Seq(a.config, a.device, a.dtype)
    run, done_in = open_dir(a, "gen", identity(a, s, manifest))
    ip, totals, t0, n = processor(True), Counter(), time.perf_counter(), 0
    todo = list(pairs(items, sample_ids(items, a.n, a.seed), a.langs, done_in))
    print(f"{a.config}: {sum(len(t) for *_, t in todo)} translations to make", flush=True)
    for src, tgt, path, ids in todo:
        if not ids:
            continue
        model, tok = s.load(src)
        cap = getattr(model.config, "max_target_positions", None) or model.config.max_position_embeddings
        special = set(tok.all_special_ids) - {model.config.eos_token_id}
        ids = sorted(ids, key=lambda i: len(items[i]["text"][src]))         # little padding per batch
        for k in range(0, len(ids), a.batch):
            chunk = ids[k:k + a.batch]
            texts = [items[i]["text"][src] for i in chunk]
            batch = ip.preprocess_batch(texts, src_lang=flores(src, manifest), tgt_lang=flores(tgt, manifest))
            max_new = [min(MAX_NEW[0] + math.ceil(MAX_NEW[1] * len(t)), cap - 1) for t in texts]
            outs, stops, ttft = greedy(model, tok, batch, max_new, a.device)
            dec = tok.batch_decode(outs, skip_special_tokens=True, clean_up_tokenization_spaces=True)
            for i, out, stop, hyp in zip(chunk, outs, stops, ip.postprocess_batch(dec, lang=flores(tgt, manifest))):
                hyp = hyp.strip()
                append_jsonl(path, dict(id=i, hyp=hyp, tokens=len(out), stop=stop, ttft=ttft,
                                        special=sum(t in special for t in out), added=0))
                totals.update(requests=1, tokens=len(out), chars=len(hyp))
            n += len(chunk)
            el = time.perf_counter() - t0
            print(f"  {src}-{tgt} {n}  {totals['tokens'] / el:.1f} tok/s  [{el:.0f} s]", flush=True)
    if not n:
        return
    import torch
    secs = time.perf_counter() - t0
    append_jsonl(run / "speed.jsonl", dict(
        totals, secs=secs, batch=a.batch, kv_blocks=None, device=a.device, dtype=a.dtype,
        weights_bytes=sum(p.numel() * p.element_size() for p in s.model.parameters()),
        gpu_peak_bytes=gpu_peak_bytes(torch.device(a.device)), footprint_peak_mib=footprint_peak_mib(),
        date=time.strftime("%Y-%m-%d %H:%M"), preempted=0, prefix_cache=None))
    append_jsonl(run / "segments.jsonl", dict(kind="gen", items=n, date=time.strftime("%Y-%m-%d %H:%M"),
                                              **code_version(engine=False)))
    print(f"{a.config}: {totals['tokens'] / secs:.1f} tok/s, {totals['chars'] / secs:.0f} chars/s over {secs:.0f} s",
          flush=True)


@no_grad()
def teacher_forced(model, tok, src: list[str], labels: list[list[int]], device) -> list[np.ndarray]:
    """-> -ln P(label token | source, the label tokens before it) per label, float64; the decoder is fed the start
    token and the labels shifted right, padded on the right (causal: padding after a row's end changes nothing)."""
    import torch
    cfg, enc_in = model.config, encode(tok, src, device)
    width = max(map(len, labels))
    dec = torch.tensor([[cfg.decoder_start_token_id] + l[:-1] + [cfg.pad_token_id] * (width - len(l)) for l in labels],
                       device=device)
    lp = model(**enc_in, decoder_input_ids=dec).logits.float().log_softmax(-1)
    return [-lp[b, torch.arange(len(l), device=device), torch.tensor(l, device=device)].double().cpu().numpy()
            for b, l in enumerate(labels)]


def references(ip, tok, refs: list[str], tgt: str, eos: int) -> tuple[list[str], list[list[int]]]:
    """References as IndicTrans2 is trained on them (IndicProcessor, no placeholders) and their target tokens + eos."""
    text = ip.preprocess_batch(refs, src_lang=tgt, is_target=True)
    return text, [x + [eos] for x in tok(text_target=text, add_special_tokens=False)["input_ids"]]


def score(a) -> None:
    items, manifest = load_data(a.data)
    s = Seq2Seq(a.config, a.device, a.dtype)
    run, done_in = open_dir(a, "score", identity(a, s, manifest))
    ip, t0, made = processor(False), time.perf_counter(), 0
    for src, tgt, path, ids in pairs(items, sample_ids(items, a.n, a.seed), a.langs, done_in):
        if not ids:
            continue
        model, tok = s.load(src)
        sl, tl = flores(src, manifest), flores(tgt, manifest)
        for k in range(0, len(ids), a.batch):
            chunk = ids[k:k + a.batch]
            refs = [items[i]["text"][tgt] for i in chunk]
            text, labels = references(ip, tok, refs, tl, model.config.eos_token_id)
            batch = ip.preprocess_batch([items[i]["text"][src] for i in chunk], src_lang=sl, tgt_lang=tl)
            back = [tok.decode(l[:-1], clean_up_tokenization_spaces=False) for l in labels]
            n_src = encode(tok, batch, "cpu")["attention_mask"].sum(1).tolist()
            for i, ref, t, l, b, nats, n in zip(chunk, refs, text, labels, back,
                                                teacher_forced(model, tok, batch, labels, a.device), n_src):
                append_jsonl(path, dict(id=i, prompt_tokens=n, ref_tokens=len(l) - 1, nats=float(nats[:-1].sum()),
                                        end_nats=float(nats[-1]), chars=len(ref), roundtrip=b == t,
                                        preprocessed=t != ref))
        made += len(ids)
        rs = read_jsonl(path)
        print(f"{src}-{tgt}: {sum(r['nats'] for r in rs) / math.log(2) / sum(r['chars'] for r in rs):.3f} "
              f"bits/char of the pre-processed reference ({len(rs)}) [{time.perf_counter() - t0:.0f} s]", flush=True)
    if made:
        append_jsonl(run / "segments.jsonl", dict(kind="score", items=made, date=time.strftime("%Y-%m-%d %H:%M"),
                                                  **code_version(engine=False)))


def parity(a) -> None:
    """--device / --dtype against CPU float32 on a few ids per direction: greedy outputs equal, and the largest
    difference in the references' per-token log-probabilities."""
    items, manifest = load_data(a.data)
    ids, ip, rows = sample_ids(items, a.n, a.seed), processor(False), []
    for src, tgt, _, todo in pairs(items, ids, a.langs, lambda s, t: (None, set())):
        sl, tl = flores(src, manifest), flores(tgt, manifest)
        batch = ip.preprocess_batch([items[i]["text"][src] for i in todo], src_lang=sl, tgt_lang=tl)
        refs = [items[i]["text"][tgt] for i in todo]
        got = {}
        for dev, dt in (("cpu", "float32"), (a.device, a.dtype)):
            model, tok = Seq2Seq("indictrans2", dev, dt).load(src)
            _, labels = references(ip, tok, refs, tl, model.config.eos_token_id)
            lp = teacher_forced(model, tok, batch, labels, dev)
            out, _, _ = greedy(model, tok, batch, [MAX_NEW[0] + math.ceil(MAX_NEW[1] * len(r)) for r in refs], dev)
            got[dev, dt] = lp, out
            del model
            gc.collect()
        (ref_lp, ref_out), (lp, out) = got.values()
        worst = max(float(np.abs(x - y).max()) for x, y in zip(ref_lp, lp))
        rows.append((f"{src}-{tgt}", sum(x == y for x, y in zip(ref_out, out)), len(out), worst))
        print(f"{src}-{tgt}: greedy outputs equal {rows[-1][1]}/{len(out)}, max |delta log p| {worst:.2e}", flush=True)
    print(f"{a.device} {a.dtype} vs cpu float32: {sum(r[1] for r in rows)}/{sum(r[2] for r in rows)} outputs equal, "
          f"max |delta log p| {max(r[3] for r in rows):.2e}")
