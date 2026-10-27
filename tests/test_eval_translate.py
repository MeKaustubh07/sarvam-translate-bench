import json
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("HF_HUB_OFFLINE", "1")
import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import eval_translate as ev

sys.path.append(str(ev.ENGINE / "tests"))
import decision
import engine
import eval_translate_report as report
import indictrans
from sacrebleu.metrics import CHRF
from serving_targets import TEMPLATE, train_tokenizer
from tokenizer import Tokenizer

torch.set_grad_enabled(False)
results = []
def check(name, ok):
    results.append(bool(ok)); print(f"{'PASS' if ok else 'FAIL'}  {name}", flush=True)


# synthetic text: English words, and the same words spelled letter for letter in each language's script
def letters(script: str) -> list[str]:
    import unicodedata
    blocks = {"Latn": (0x61, 0x7B), "Arab": (0x620, 0x64B), "Mtei": (0xABC0, 0xABDB), "Olck": (0x1C5A, 0x1C78)}
    lo, hi = blocks.get(script, (0x900, 0xD80))
    return [chr(c) for c in range(lo, hi) if unicodedata.category(chr(c)) == "Lo"
            and unicodedata.name(chr(c), "").startswith(ev.SCRIPTS[script] + " LETTER")]


WORDS = "the river city school market rain festival court train doctor music field".split()
SCRIPT_OF = {"eng": "Latn", "asm": "Beng", "ben": "Beng", "guj": "Gujr", "kan": "Knda", "kas": "Arab", "mal": "Mlym",
             "mni": "Mtei", "ory": "Orya", "pan": "Guru", "sat": "Olck", "tam": "Taml", "tel": "Telu", "urd": "Arab"}
DOMAINS = ["culture", "economy", "education", "entertainment", "geography", "governments", "health", "industry",
           "legal", "news", "religion", "sports", "tourism"]


def spell(text: str, script: str) -> str:
    al = letters(script)
    return "".join(al[(ord(ch) - 97) % len(al)] if ch.isalpha() else ch for ch in text)


rng = np.random.default_rng(0)
rows = []
for k in range(104):                                   # 13 domains x 2 sources x 4
    en = " ".join(rng.choice(WORDS, size=int(rng.integers(3, 6)))).capitalize() + "."
    row = dict(id=k + 1, context="ctx", source=("web", "wikipedia")[k % 2], url="", domain=DOMAINS[k // 2 % 13],
               num_words=len(en.split()), bucket="1 - 10")
    for code in ev.NAMES:
        script = SCRIPT_OF.get(code, "Deva")
        row[f"sentence_{code}_{script}"] = en if code == "eng" else spell(en.lower(), script)
    row["sentence_mni_Beng"] = spell(en.lower(), "Beng")   # a second script for Manipuri: Meitei is picked
    rows.append(row)

tmp = tempfile.TemporaryDirectory()
T = Path(tmp.name)
D, R, O = T / "data", T / "runs", T / "out"

# 1. data: the parquet through cmd_data, the download stubbed
import huggingface_hub
import pyarrow as pa
import pyarrow.parquet as pq
(T / "dl/data").mkdir(parents=True)
pq.write_table(pa.Table.from_pylist(rows), T / "dl/data/train.parquet")
huggingface_hub.hf_hub_download = lambda *a, **k: str(T / "dl/data/train.parquet")
ev.IN22 = dict(ev.IN22, sha256=ev.sha256(T / "dl/data/train.parquet"))
ev.main(["data", "--data", str(D)])
items, man = ev.load_data(str(D))
langs = man["languages"]
check("data: 104 rows, all 23 languages found, Manipuri in Meitei (Bengali-script column kept as the alternative)",
      len(items) == 104 and set(langs) == set(ev.NAMES) and langs["mni"]["script"] == "Mtei"
      and langs["mni"]["other_scripts"] == ["Beng"] and langs["snd"]["column"] == "sentence_snd_Deva")
check("data: every language's text is in its column's script (letters), none empty",
      all(v["script_share"] == 1.0 and v["empty"] == 0 for v in langs.values()))
check("data: 26 strata of 4 ids; metadata kept, the context dropped",
      len(man["strata"]) == 26 and set(man["strata"].values()) == {4} and "context" not in items[1]
      and items[1]["domain"] == "culture")
bad = []
for drop, add in (("sentence_mni_Mtei", {}), (None, {"sentence_hin_Latn": "x"})):
    try:
        ev.write_dataset([{k: v for k, v in r.items() if k != drop} | add for r in rows[:2]], T / "bad", ev.IN22)
        bad.append(False)
    except ValueError:
        bad.append(True)
check("data: a multi-script language without its prompt's column, and a second script for another, are refused",
      all(bad))
(D / "in22_gen.jsonl").write_text((D / "in22_gen.jsonl").read_text().replace("River", "Rivers", 1))
try:
    ev.load_data(str(D)); refused = False
except SystemExit:
    refused = True
check("data: a changed in22_gen.jsonl is refused (SHA-256 in the manifest)", refused)
ev.main(["data", "--data", str(D)])                     # rewritten from the parquet
ev.IN22["sha256"] = "0" * 64
try:
    ev.main(["data", "--data", str(D)]); refused = False
except SystemExit:
    refused = True
check("data: a parquet that is not the pinned one is refused", refused)
items, man = ev.load_data(str(D))

# 2. the sample
s26, s200, s50 = ev.sample_ids(items, 26, 0), ev.sample_ids(items, 200, 0), ev.sample_ids(items, 50, 0)
cells = {(items[i]["domain"], items[i]["source"]) for i in s26}
check("sample: seeded (same order twice), nested (n=50 is the first 50 of n=200), another seed differs",
      s50 == ev.sample_ids(items, 50, 0) == s200[:50] and len(s200) == 104 and ev.sample_ids(items, 50, 1) != s50)
check("sample: stratified (26 ids hit all 26 domain x source cells once)", len(cells) == 26 and len(set(s26)) == 26)

# 3. prompts through the real chat templates == transformers'
from transformers import AutoTokenizer
TEXT = {"eng": "The court opened the river festival in 2026.", "mni": "ꯃꯤꯇꯩꯂꯣꯟ ꯑꯁꯤ ꯌꯥꯝꯅ ꯐꯖꯩ꯫", "hin": "नदी उत्सव।"}
for model in ("sarvam-translate", "gemma-3-4b-it"):
    d = engine.ROOT / engine.MODELS[model]["dir"]
    if not (d / "tokenizer.json").exists():
        print(f"SKIP  prompts of {model}: no tokenizer files"); continue
    tok, hf = Tokenizer(str(d / "tokenizer.json")), AutoTokenizer.from_pretrained(str(d))
    eng = SimpleNamespace(name=model, chat_style=engine.chat_style(engine.MODELS[model], d), tokenizer=tok,
                          eos_ids=set(engine.MODELS[model]["eos"]))
    special, added = ev.added_tokens(model)
    eoa = ev.end_of_answer(eng)
    ok = [eoa == 106, eoa in special]
    for src, tgt in (("eng", "hin"), ("eng", "mni"), ("mni", "eng")):
        for style in ("card", "neutral"):
            p = ev.prompt(eng, src, tgt, TEXT[src], style)
            names = (ev.NAMES[src], ev.NAMES[tgt]) if style == "card" else (ev.label(src), ev.label(tgt))
            ref = hf.apply_chat_template(ev.messages(style, *names, TEXT[src]), tokenize=False,
                                         add_generation_prompt=True)
            ids = tok.encode(p)
            ok += [p == ref, ids == hf(ref, add_special_tokens=False)["input_ids"], ids.count(tok.bos_id) == 1,
                   p.startswith(f"<bos><start_of_turn>user\nTranslate the text below to {ev.NAMES[tgt]}.\n\n"
                                f"{TEXT[src]}<end_of_turn>\n<start_of_turn>model\n") if style == "card" else
                   f"Translate the following text from {names[0]} to {names[1]}. Reply with the translation "
                   f"only.\n\n{TEXT[src]}" in p and ("Manipuri (Meitei Mayek script)" in p) == ("mni" in (src, tgt))]
    check(f"prompts: {model} == apply_chat_template (text and ids, BOS once): the card's system turn folded into the "
          f"user's, and the neutral control, both directions; end of answer {eoa}, a special token", all(ok))

# 3b. the weights' INT4 policy, from .qt headers or the registry's policy file (no model is loaded)
def fake_qt(path, schemes, scheme="int4"):
    """A .qt header without data: the tied embedding first (INT8 in every INT4 file), then layer tensors."""
    names = ["model.embed_tokens.weight"] + [f"model.layers.{k}.mlp.down_proj.weight" for k in range(len(schemes) - 1)]
    head = json.dumps({"__metadata__": {"scheme": scheme, "block": "32"}} | {
        f"{n}::q": {"dtype": "U8", "shape": [1, 1], "data_offsets": [0, 0], "scheme": s} for n, s in zip(names, schemes)})
    path.write_bytes(len(head).to_bytes(8, "little") + head.encode())
    return str(path)


def refused(fn):
    try:
        fn(); return False
    except SystemExit:
        return True


mixed, flat = fake_qt(T / "mixed.qt", ["int8", "int4", "int8", "int4"]), fake_qt(T / "flat.qt", ["int8", "int4", "int4"])
int8 = fake_qt(T / "int8.qt", ["int8", "int8"], "int8")
ev.CONFIGS["sarvam-int4-flat"] = ("sarvam-translate", "metal-int4", "flat")   # an INT4 ablation, not compared
spec, pol = engine.MODELS["sarvam-translate"], T / "policy.json"
pol.write_text("{}")
saved = spec.get("policy")
w_mixed, w_flat = ev.weights_identity("sarvam-int4", mixed), ev.weights_identity("sarvam-int4-flat", flat)
spec["policy"] = str(T / "absent.json")
no_policy = ev.weights_identity("sarvam-int4-flat", None)
ok = [w_mixed["schemes"] == {"int4": 2, "int8": 2} and w_mixed["policy_int8"] == 1 and len(w_mixed["header_sha256"]) == 64,
      w_flat["schemes"] == {"int8": 1, "int4": 2} and w_flat["policy_int8"] == 0,
      refused(lambda: ev.weights_identity("sarvam-int4", flat)),
      refused(lambda: ev.weights_identity("sarvam-int4-flat", mixed)),
      refused(lambda: ev.weights_identity("sarvam-int4", int8)), ev.weights_identity("sarvam-int8", int8)["file"],
      refused(lambda: ev.weights_identity("sarvam-int4", None)), no_policy["policy"] is None]
spec["policy"] = str(pol)
ok += [ev.weights_identity("sarvam-int4", None)["policy_sha256"] == ev.sha256(pol),
       refused(lambda: ev.weights_identity("sarvam-int4-flat", None)),
       ev.weights_identity("sarvam-int8", None)["policy"] is None]
spec["policy"] = saved
del ev.CONFIGS["sarvam-int4-flat"]
check("weights: calibrated INT4 refuses flat weights and flat refuses calibrated (INT8 tensors beyond the tied "
      "embedding in the .qt, or a policy file at load); a file of another scheme refused; identity holds the header "
      "SHA-256 and scheme counts, or the policy's SHA-256", all(ok))

# 4. a tiny Gemma 3 in a fake registry entry: generate, resume, score
import tiny_gemma3

d = T / "tiny-gemma3"
d.mkdir()
train_tokenizer(str(d / "tokenizer.json"))                   # the test template: <|end|> ends a turn
json.dump({"chat_template": TEMPLATE, "bos_token": "<bos>", "eos_token": "<eos>"}, open(d / "tokenizer_config.json", "w"))
tiny_gemma3.build(str(d), window=16)
t = Tokenizer(str(d / "tokenizer.json"))
engine.MODELS["tiny-gemma3-eval"] = dict(dir=str(d), family="gemma3", weights="model.safetensors", chat="template",
                                         eos=[t.special["<eos>"], t.special["<|end|>"]], sampling={}, max_model_len=2048)
ev.CONFIGS["tiny-gemma3"] = ("tiny-gemma3-eval", "cpu", None)
COMMON = ["--data", str(D), "--runs", str(R), "--langs", "hin,mni"]


def gen_lines(cfg):
    return {f.stem: ev.read_jsonl(f) for f in sorted((R / cfg / "gen").glob("*.jsonl"))}


def outputs(cfg):
    """Each direction's records without their timing, in file order."""
    return {k: [json.dumps({f: x for f, x in r.items() if f != "ttft"}) for r in v] for k, v in gen_lines(cfg).items()}


def greedy(eng, ids, max_new):
    st, out = eng.model.new_state(len(ids) + max_new), []
    lg = eng.model.forward(torch.tensor(ids), state=st, last_only=True)[0]
    while len(out) < max_new and (nxt := int(lg[:eng.tokenizer.vocab_size()].argmax())) not in eng.eos_ids:
        out.append(nxt)
        lg = eng.model.forward(torch.tensor([nxt]), state=st, last_only=True)[0]
    return out


for cfg in ("tiny-gemma3",):
    ev.main(["generate", cfg, *COMMON, "--n", "6", "--batch", "4", "--kv-blocks", "128"])
    g = gen_lines(cfg)
    speed, seg = ev.read_jsonl(R / cfg / "speed.jsonl"), ev.read_jsonl(R / cfg / "segments.jsonl")
    check(f"{cfg} generate: 4 directions x 6 ids, every record complete, one speed record of 24 requests, one segment "
          "with its code version",
          sorted(g) == ["eng-hin", "eng-mni", "hin-eng", "mni-eng"] and all(len(v) == 6 for v in g.values())
          and all(set(r) == {"id", "hyp", "tokens", "stop", "ttft", "special", "added"} for v in g.values() for r in v)
          and len(speed) == 1 and speed[0]["requests"] == 24 and speed[0]["tokens"] > 0
          and len(seg) == 1 and seg[0]["kind"] == "gen" and seg[0]["items"] == 24 and len(seg[0]["code_sha256"]) == 16)
    args = SimpleNamespace(config=cfg, weights=None, runs=str(R), prompt=None, seed=0)
    eng, run, _ = ev.open_run(args, "gen", man)
    meta = json.load(open(run / "meta.json"))
    check(f"{cfg} generate: meta records the prompt messages (the card's), the rendered template, the seed, the "
          "dataset and the end-of-answer token", meta["config"] == cfg and meta["prompt"] == "card"
          and meta["messages"][0]["role"] == "system" and "{text}" in meta["example_prompt"]
          and meta["seed"] == 0 and meta["dataset"] == man["jsonl_sha256"]
          and meta["end_of_answer"] == eng.tokenizer.special["<|end|>"] and meta["weights"]["file"] is None)
    special, added = ev.added_tokens(eng.name)
    same, stripped = True, 0
    for d_, recs in g.items():
        src, tgt = d_.split("-")
        for r in recs[:3]:
            text = items[r["id"]]["text"][src]
            ids = eng.tokenizer.encode(ev.prompt(eng, src, tgt, text))
            max_new = min(ev.MAX_NEW[0] + int(np.ceil(ev.MAX_NEW[1] * len(text))), 2048 - len(ids))
            out = greedy(eng, ids, max_new)
            keep = [t for t in out if t not in special]
            stripped += len(out) - len(keep)
            same &= eng.tokenizer.decode(keep).strip() == r["hyp"] and len(out) == r["tokens"] \
                and r["stop"] == ("length" if len(out) == max_new else "stop") \
                and r["special"] == len(out) - len(keep) and r["added"] == sum(t in added for t in keep)
    check(f"{cfg} generate: batched through the scheduler == a sequential greedy loop (12 items, tokens, stop), special "
          f"tokens removed and counted ({stripped})", same)

    before = outputs(cfg)
    ev.main(["generate", cfg, *COMMON, "--n", "6", "--batch", "4", "--kv-blocks", "128"])
    check(f"{cfg} resume: a rerun makes nothing (files, speed records and segments unchanged)",
          outputs(cfg) == before and len(ev.read_jsonl(R / cfg / "speed.jsonl")) == 1
          and len(ev.read_jsonl(R / cfg / "segments.jsonl")) == 1)
    f = R / cfg / "gen" / "hin-eng.jsonl"
    f.write_bytes(torn := f.read_bytes()[:-7])          # the last record torn mid-line
    check(f"{cfg} read_jsonl: a torn last line is skipped and the file left as it is",
          len(ev.read_jsonl(f)) == 5 and f.read_bytes() == torn)
    ev.main(["generate", cfg, *COMMON, "--n", "6", "--batch", "4", "--kv-blocks", "128"])
    speed = ev.read_jsonl(R / cfg / "speed.jsonl")
    after = outputs(cfg)
    check(f"{cfg} resume: the writer cuts a torn last line and makes only that item again, identical",
          len(speed) == 2 and speed[1]["requests"] == 1 and sorted(after["hin-eng"]) == sorted(before["hin-eng"])
          and all(after[k] == before[k] for k in before if k != "hin-eng"))

    ev.main(["score", cfg, *COMMON, "--n", "6"])
    sc = {f.stem: ev.read_jsonl(f) for f in sorted((R / cfg / "score").glob("*.jsonl"))}
    worst, eoa = 0.0, meta["end_of_answer"]
    for d_, recs in sc.items():
        src, tgt = d_.split("-")
        for r in recs:
            p = eng.tokenizer.encode(ev.prompt(eng, src, tgt, items[r["id"]]["text"][src]))
            c = eng.tokenizer.encode(items[r["id"]]["text"][tgt])
            lp = torch.log_softmax(eng.model.forward(torch.tensor(p + c + [eoa])).double(), -1)
            hand = -sum(lp[len(p) - 1 + k, t].item() for k, t in enumerate(c))
            end = -torch.logsumexp(lp[len(p) - 1 + len(c), sorted(eng.eos_ids)], 0).item()
            worst = max(worst, abs(r["nats"] - hand) / hand, abs(r["end_nats"] - end) / end)
            worst = worst if r["ref_tokens"] == len(c) else float("inf")
    check(f"{cfg} score: nats and end_nats == -log p from full-sequence logits (24 references and their "
          f"P(any stop) at the end, worst rel {worst:.1e} < 1e-5); one score segment",
          len(sc) == 4 and all(len(v) == 6 for v in sc.values()) and worst < 1e-5
          and all(r["roundtrip"] and r["chars"] == len(items[r["id"]]["text"][k.split("-")[1]])
                  for k, v in sc.items() for r in v)
          and [x["kind"] for x in ev.read_jsonl(R / cfg / "segments.jsonl")] == ["gen", "gen", "score"])
    seqs = [(r["id"], eng.tokenizer.encode(ev.prompt(eng, "eng", "mni", items[r["id"]]["text"]["eng"])),
             eng.tokenizer.encode(items[r["id"]]["text"]["mni"]) + [eoa]) for r in sc["eng-mni"]]
    packed = dict(ev.teacher_forced(eng.model, seqs, eng.tokenizer.vocab_size()))
    budget, decision.FORK_BUDGET = decision.FORK_BUDGET, 1
    alone = dict(ev.teacher_forced(eng.model, seqs, eng.tokenizer.vocab_size()))
    decision.FORK_BUDGET = budget
    common = len(os.path.commonprefix([p for _, p, _ in seqs]))
    check(f"{cfg} score: packed forks == one at a time, token by token (common prefix {common} tokens)",
          all(len(packed[k]) == len(c) and np.allclose(packed[k], alone[k], rtol=1e-5, atol=1e-6)
              for (k, _, c) in seqs))
    json.dump(meta | {"weights": "another.qt"}, open(run / "meta.json", "w"))
    other = refused(lambda: ev.open_run(args, "gen", man))
    json.dump(meta, open(run / "meta.json", "w"))
    check(f"{cfg}: results of another build, or of another seed, in the same run directory are refused",
          other and refused(lambda: ev.open_run(SimpleNamespace(**vars(args) | {"seed": 1}), "gen", man)))

# 4b. the seq2seq (IndicTrans2) path: language tags, and a tiny random encoder-decoder through generate and score
real = json.load(open(ev.DATA / "manifest.json")) if (ev.DATA / "manifest.json").exists() else None
tags = {x: indictrans.flores(x, man) for x in ev.NAMES}
check("indictrans2: every IN22-Gen language maps to an IndicTrans2 tag in its column's script (Manipuri mni_Mtei, "
      "Santali sat_Olck, Sindhi snd_Deva, Kashmiri kas_Arab); another script is refused"
      + ("; the real manifest's too" if real else " (SKIP the real manifest: no data/in22-gen)"),
      set(tags.values()) <= indictrans.CODES and len(set(tags.values())) == len(ev.NAMES)
      and [tags[x] for x in ("mni", "sat", "snd", "kas", "eng")] == ["mni_Mtei", "sat_Olck", "snd_Deva", "kas_Arab",
                                                                      "eng_Latn"]
      and refused(lambda: indictrans.flores("mni", {"languages": {"mni": {"script": "Latn"}}}))
      and (real is None or all(indictrans.flores(x, real) == tags[x] for x in ev.NAMES)))
ip = indictrans.processor(True)
pre = ip.preprocess_batch(["Call me on 12/05/2026."], src_lang="eng_Latn", tgt_lang="mni_Mtei")
post = ip.postprocess_batch(["ꯃꯤꯇꯩ <ID1> ꯑꯁꯤ"], lang="mni_Mtei")
check(f"indictrans2: IndicProcessor (the installed IndicTransToolkit, its __init__ skipped) writes both tags first "
      f"and wraps numbers in placeholders that postprocess restores ({pre[0]!r})",
      pre == ["eng_Latn mni_Mtei Call me on < ID1 > ."] and post == ["ꯃꯤꯇꯩ 12/05/2026 ꯑꯁꯤ"])


def tiny_seq2seq(d: Path, seed: int) -> None:
    """A random M2M100 (the fairseq transformer IndicTrans2 copies: sinusoidal positions, scaled embeddings, decoder
    start = eos) with a byte-level BPE, saved as transformers loads it."""
    from transformers import M2M100Config, M2M100ForConditionalGeneration, PreTrainedTokenizerFast
    d.mkdir()
    train_tokenizer(str(d / "tokenizer.json"))
    tok = PreTrainedTokenizerFast(tokenizer_file=str(d / "tokenizer.json"), pad_token="<pad>", bos_token="<bos>",
                                  eos_token="<eos>")
    tok.save_pretrained(d)
    torch.manual_seed(seed)
    M2M100ForConditionalGeneration(M2M100Config(
        vocab_size=len(tok), d_model=64, encoder_layers=2, decoder_layers=2, encoder_attention_heads=4,
        decoder_attention_heads=4, encoder_ffn_dim=128, decoder_ffn_dim=128, max_position_embeddings=1024,
        pad_token_id=tok.pad_token_id, bos_token_id=tok.bos_token_id, eos_token_id=tok.eos_token_id,
        decoder_start_token_id=tok.eos_token_id, init_std=0.5, dropout=0.0)).save_pretrained(d)


for side, seed in (("en-x", 1), ("x-en", 2)):
    tiny_seq2seq(T / f"tiny-it2-{side}", seed)
indictrans.HF["tiny-it2"] = {side: str(T / f"tiny-it2-{side}") for side in ("en-x", "x-en")}
ev.CONFIGS["tiny-it2"] = ("tiny-it2", "hf", None)
HF_ARGS = ["--device", "cpu", "--dtype", "float32"]
ev.main(["generate", "tiny-it2", *COMMON, *HF_ARGS, "--n", "6", "--batch", "4"])
g, eng_g = gen_lines("tiny-it2"), gen_lines("tiny-gemma3")
meta = json.load(open(R / "tiny-it2" / "meta.json"))
check("tiny-it2 generate: the engine's directions, ids and record fields; one speed record (24 requests, the stack's "
      "device and dtype), one segment; meta: no prompt, the tags as the example, the text bits are of",
      sorted(g) == sorted(eng_g) and all(sorted(r["id"] for r in g[k]) == sorted(r["id"] for r in eng_g[k]) for k in g)
      and all(set(r) == set(eng_g["eng-hin"][0]) for v in g.values() for r in v)
      and (sp := ev.read_jsonl(R / "tiny-it2" / "speed.jsonl"))[0]["requests"] == 24 and len(sp) == 1
      and sp[0]["device"] == "cpu" and len(ev.read_jsonl(R / "tiny-it2" / "segments.jsonl")) == 1
      and meta["messages"] is None and meta["example_prompt"] == "eng_Latn mni_Mtei TEXT"
      and meta["bpc_text"] == indictrans.BPC_TEXT and meta["weights"]["en-x"]["config_sha256"])
s2s = indictrans.Seq2Seq("tiny-it2", "cpu", "float32")
same = True
for k, recs in g.items():
    src, tgt = k.split("-")
    model, tok = s2s.load(src)
    for r in recs[:3]:                                       # alone: no padding, the same tokens and text
        text = items[r["id"]]["text"][src]
        b = ip.preprocess_batch([text], src_lang=tags[src], tgt_lang=tags[tgt])
        cap = ev.MAX_NEW[0] + int(np.ceil(ev.MAX_NEW[1] * len(text)))
        ids = tok(b, return_tensors="pt")["input_ids"]
        cur = torch.tensor([[model.config.decoder_start_token_id]])
        out = []
        while len(out) < cap:                                # no cache: the whole prefix each step
            nxt = int(model(input_ids=ids, decoder_input_ids=cur).logits[0, -1].argmax())
            if nxt == model.config.eos_token_id:
                break
            out.append(nxt)
            cur = torch.cat([cur, torch.tensor([[nxt]])], 1)
        hyp = ip.postprocess_batch([tok.decode(out, skip_special_tokens=True, clean_up_tokenization_spaces=True)],
                                   lang=tags[tgt])[0].strip()
        same &= out != [] and len(out) == r["tokens"] and hyp == r["hyp"] and r["stop"] == (
            "length" if len(out) == cap else "stop")
check("tiny-it2 generate: batched greedy with the KV cache == one source at a time without it (12 items: tokens, "
      "stop, post-processed text)", same)
before = outputs("tiny-it2")
ev.main(["generate", "tiny-it2", *COMMON, *HF_ARGS, "--n", "6", "--batch", "4"])
check("tiny-it2 resume: a rerun makes nothing; another dtype in the same run directory is refused",
      outputs("tiny-it2") == before and len(ev.read_jsonl(R / "tiny-it2" / "speed.jsonl")) == 1
      and refused(lambda: ev.main(["generate", "tiny-it2", *COMMON, "--device", "cpu", "--dtype", "bfloat16"])))
ev.main(["score", "tiny-it2", *COMMON, *HF_ARGS, "--n", "6", "--batch", "4"])
sc = {f.stem: ev.read_jsonl(f) for f in sorted((R / "tiny-it2" / "score").glob("*.jsonl"))}
worst, ip0 = 0.0, indictrans.processor(False)
for k, recs in sc.items():
    src, tgt = k.split("-")
    model, tok = s2s.load(src)
    for r in recs:
        b = ip0.preprocess_batch([items[r["id"]]["text"][src]], src_lang=tags[src], tgt_lang=tags[tgt])
        ref = ip0.preprocess_batch([items[r["id"]]["text"][tgt]], src_lang=tags[tgt], is_target=True)[0]
        lab = tok(text_target=ref, add_special_tokens=False)["input_ids"] + [model.config.eos_token_id]
        lp = torch.log_softmax(model(input_ids=tok([b[0]], return_tensors="pt")["input_ids"], decoder_input_ids=torch.tensor(
            [[model.config.decoder_start_token_id] + lab[:-1]])).logits[0].double(), -1)
        nll = -lp[torch.arange(len(lab)), torch.tensor(lab)]
        worst = max(worst, abs(r["nats"] - nll[:-1].sum().item()) / nll[:-1].sum().item(),
                    abs(r["end_nats"] - nll[-1].item()) / nll[-1].item())
        worst = worst if r["ref_tokens"] == len(lab) - 1 and r["chars"] == len(items[r["id"]]["text"][tgt]) else 1.0
check(f"tiny-it2 score: nats and end_nats (eos) == -log p of the pre-processed reference from one unpadded forward "
      f"(24 references, worst rel {worst:.1e} < 1e-5); flags: tokens decode back, reference changed by the processor",
      len(sc) == 4 and all(len(v) == 6 for v in sc.values()) and worst < 1e-5
      and all(r["roundtrip"] for v in sc.values() for r in v)
      and all(r["preprocessed"] for v in sc.values() for r in v))       # every synthetic sentence ends in "."

# 5. report: chrF++ on IN22's protocol vs sacrebleu, macro rows, diagnostics; files read, never written
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
from indicnlp.tokenize.indic_tokenize import trivial_tokenize


def in22(text, tgt):
    """IndicTrans2's preprocess_translate.py for hin_Deva and mni_Mtei (both "hi" in its code map); English raw."""
    if tgt == "eng":
        return text
    return " ".join(trivial_tokenize(IndicNormalizerFactory().get_normalizer("hi").normalize(text.strip()), "hi"))


def snapshot():
    return {f: f.read_bytes() for f in sorted(R.rglob("*")) if f.is_file()}


f = R / "tiny-it2" / "gen" / "eng-hin.jsonl"
f.write_bytes(f.read_bytes() + b'{"id": 99, "hy')     # a record being written while the report reads
files = snapshot()
ev.main(["report", "--data", str(D), "--runs", str(R), "--out", str(O), "--boot", "200", "--baseline", "tiny-gemma3"])
check("report: reads only (every run file byte-identical after it, a line being written skipped)", snapshot() == files)
f.write_bytes(f.read_bytes()[:f.read_bytes().rfind(b"\n") + 1])
num = json.load(open(O / "numbers.json"))
chrf = CHRF(word_order=2)
TINY = ("tiny-gemma3", "tiny-it2")
ok, diag = [], []
for cfg in TINY:
    for d_, recs in gen_lines(cfg).items():
        tgt = d_.split("-")[1]
        ok.append(abs(num["chrf"][d_][cfg]["score"] - chrf.corpus_score(
            [in22(r["hyp"], tgt) for r in recs], [[in22(items[r["id"]]["text"][tgt], tgt) for r in recs]]).score) < 1e-9)
        diag.append(num["diagnostics"][cfg][d_] == dict(
            outputs=len(recs), wrong_script=sum(ev.script_share(r["hyp"], man["languages"][tgt]["script"]) < 0.5
                                                for r in recs),
            length_stops=sum(r["stop"] == "length" for r in recs), special=sum(r["special"] > 0 for r in recs),
            added=sum(r["added"] > 0 for r in recs)))
md = (O / "tables.md").read_text()
mac = num["macro"]["chrf"]["English -> X"]
check("report: tables.md, numbers.json / .csv and chrf.svg written; chrF++ == sacrebleu's corpus_score on IN22's "
      "protocol (IndicNLP normalize + trivial_tokenize); signature and protocol printed",
      all(ok) and len(ok) == 8 and "nc:6|nw:2" in md and "version:2.6.0" in md and report.PROTOCOL in md
      and ET.parse(O / "chrf.svg").getroot().tag.endswith("svg") and num["protocol"] == report.PROTOCOL
      and len((O / "numbers.csv").read_text().splitlines()) == 1 + sum(
          len(cl) for m in ("chrf", *report.BPC) for cl in num[m].values()) + sum(
          len(v["configs"]) for m in num["macro"].values() for side in m.values() for v in side.values())
      and "delta" in num["chrf"]["eng-hin"]["tiny-it2"] and num["ids"]["eng-hin"] == sorted(ev.sample_ids(items, 6, 0)))
check("report: macro rows over all languages (2) and one script (1: not Manipuri), each with paired CIs; bits per "
      "character with the end-of-answer token above those without",
      all(f"**macro, {n}**" in md for n in ("all (2)", "one script (1)"))
      and mac["all"]["langs"] == ["hin", "mni"] and mac["one script"]["langs"] == ["hin"]
      and "ci" in mac["all"]["configs"]["tiny-it2"] and "ci" not in mac["all"]["configs"]["tiny-gemma3"]
      and all(num["bpc_end"][d_][c]["score"] > num["bpc"][d_][c]["score"] for d_ in num["bpc"] for c in num["bpc"][d_]))
check("report: the seq2seq config's bits (of its pre-processed reference) stay out of the comparable bits tables and "
      "are reported apart, marked NOT comparable; its tokens per character listed; the speed table names each stack",
      all(set(num[m][d_]) == {"tiny-gemma3"} for m in ("bpc", "bpc_end") for d_ in num[m])
      and all(set(num["bpc_pre"][d_]) == {"tiny-it2"} for d_ in num["bpc_pre"]) and len(num["bpc_pre"]) == 4
      and "NOT comparable" in md and set(num["tokens_per_char"]) == set(TINY)
      and "| tiny-it2 | hf cpu float32 |" in md and "| tiny-gemma3 | cpu |" in md)
check("report: per-direction diagnostics == a recount of the records (wrong script per output, length stops, special "
      "and other added tokens), the directions with any listed", all(diag) and len(diag) == 8
      and all((f"| {c} | {d_} |" in md) == any(list(v.values())[1:]) for c in TINY
              for d_, v in num["diagnostics"][c].items()))
check("report: code versions per config; a warning only when a config's segments differ",
      all(len(num["code"][c]) >= 1 for c in TINY)
      and ("**Warning:**" in md) == any(len(num["code"][c]) > 1 for c in TINY))
check("report: an unknown --baseline is refused", refused(lambda: ev.main(
    ["report", "--data", str(D), "--runs", str(R), "--out", str(T / "o3"), "--baseline", "nope"])))

# the prompt-swap control: its own run directory, a config of its own in the report
ev.main(["generate", "tiny-gemma3", "--data", str(D), "--runs", str(R), "--langs", "hin", "--n", "3", "--batch", "2",
         "--kv-blocks", "64", "--prompt", "neutral"])
ctl = R / "tiny-gemma3@neutral"
cmeta = json.load(open(ctl / "meta.json"))
ev.main(["report", "--data", str(D), "--runs", str(R), "--out", str(T / "o2"), "--boot", "50"])
num2 = json.load(open(T / "o2" / "numbers.json"))
mac2 = num2["macro"]["chrf"]["English -> X"]
check("control: --prompt neutral on the card model -> RUNS/tiny-gemma3@neutral (neutral user turn); the report "
      "(no --baseline: the first config) leaves it out of the macro over all languages and keeps it in Hindi's",
      cmeta["prompt"] == "neutral" and cmeta["messages"][0]["role"] == "user"
      and sorted(gen_lines("tiny-gemma3@neutral")) == ["eng-hin", "hin-eng"] and num2["baseline"] == "tiny-gemma3"
      and "tiny-gemma3@neutral" not in mac2["all"]["configs"] and "ci" in mac2["one script"]["configs"][
          "tiny-gemma3@neutral"] and "tiny-gemma3@neutral" in num2["chrf"]["eng-hin"])

# 6. the protocol on canonically equal text, the bootstrap
import unicodedata
nfc = unicodedata.normalize("NFC", "क़ानून और फ़ैसला सड़क पर हुआ।")
pre = nfc.replace("क़", "क़").replace("फ़", "फ़").replace("ड़", "ड़")
hi = report.in22_preprocess("hin", "Deva")
raw, prot = chrf.sentence_score(nfc, [pre]).score, chrf.sentence_score(hi(nfc), [hi(pre)]).score
danda = chrf.sentence_score(hi("सड़क पर हुआ।"), [hi("सड़क पर हुआ ।")]).score
urd = report.in22_preprocess("urd", "Arab")("یہ ایک کتاب ہے۔")
check(f"protocol: precomposed nukta letters vs their NFC form score 100 (raw {raw:.1f}); a danda attached or spaced "
      "100; Urdu through urduhack's normalizer (its TensorFlow package init skipped); English raw",
      pre != nfc and unicodedata.normalize("NFC", pre) == nfc and prot == 100 and raw < 60 and danda == 100
      and urd.endswith(" ۔") and report.in22_preprocess("eng", "Latn")(" A b. ") == " A b. ")

hyps, refs = [], []
for k in range(40):                                    # Indic and English pairs with word and character edits
    ref = items[k + 1]["text"]["hin" if k % 2 else "eng"]
    hyp = " ".join(ref.split()[::-1]) if k % 3 == 0 else ref[: max(1, len(ref) - k % 5)]
    hyps.append(hyp); refs.append(ref)
(T / "hyp.txt").write_text("\n".join(hyps) + "\n"); (T / "ref.txt").write_text("\n".join(refs) + "\n")
cli = subprocess.run([sys.executable, "-m", "sacrebleu", str(T / "ref.txt"), "-i", str(T / "hyp.txt"), "-m", "chrf",
                      "--chrf-word-order", "2", "-b", "-w", "6"], capture_output=True, text=True).stdout.strip()
fn = lambda s: chrf._compute_score_from_stats(list(s)).score
stats = np.array(chrf._extract_corpus_statistics(hyps, [refs]))
ids = list(range(40))
other = np.array(chrf._extract_corpus_statistics(refs[:20] + hyps[20:], [refs]))
per = {"a": {"d": (ids, stats)}, "b": {"d": (ids, other)}, "c": {"d": (ids, stats)}}
r1, r2, r3 = (report.compare(per, fn, 300, s, "a") for s in (7, 7, 8))
check(f"chrF++ of 40 pairs == sacrebleu's CLI ({cli})", cli and abs(r1["d"]["a"]["score"] - float(cli)) < 1e-6)
check("bootstrap: the same seed gives the same CIs, another seed others; a system against itself: delta 0, CI [0, 0]; "
      "lo <= delta <= hi", r1["d"]["b"]["ci"] == r2["d"]["b"]["ci"] and r1["d"]["b"]["ci"] != r3["d"]["b"]["ci"]
      and r1["d"]["c"]["ci"] == [0.0, 0.0] and r1["d"]["c"]["delta"] == 0
      and r1["d"]["b"]["ci"][0] <= r1["d"]["b"]["delta"] <= r1["d"]["b"]["ci"][1])


def correlated(rng, dirs=22, n=50):
    """Two configs' bits per character in `dirs` directions over the same n ids, each sentence's difficulty shared by
    every direction (and larger for b): the case IN22-Gen's n-way parallel sample makes."""
    chars, shared, per = rng.integers(60, 200, n), rng.normal(0, 1, n), {"a": {}, "b": {}}
    for d in range(dirs):
        a = 2.0 + .3 * shared + rng.normal(0, .3, n)
        b = a + .1 + .4 * shared + rng.normal(0, .3, n)
        per["a"][f"d{d:02d}"] = (list(range(n)), np.stack([a * chars, chars], 1))
        per["b"][f"d{d:02d}"] = (list(range(n)), np.stack([b * chars, chars], 1))
    return per


ratio = lambda s: float(s[0] / s[1])
rng, deltas, widths = np.random.default_rng(1), [], []
for t in range(150):
    m = report.macro(per := correlated(rng), ratio, sorted(per["a"]), 200, t, "a")
    deltas.append(m["b"]["delta"]); widths.append(m["b"]["ci"][1] - m["b"]["ci"][0])
spread = float(np.diff(np.percentile(deltas, [2.5, 97.5]))[0])
per["c"] = per["a"]
m, q = report.macro(per, ratio, sorted(per["a"]), 200, 0, "a"), report.compare(per, ratio, 200, 0, "a")
check(f"macro bootstrap: the CI of a macro delta ({np.mean(widths):.3f} wide on average) covers the spread of the delta "
      f"over 150 fresh samples ({spread:.3f}) when sentence difficulty is shared across directions; the mean of the "
      "directions' scores; a config against itself: CI [0, 0]",
      0.75 < np.mean(widths) / spread < 1.4 and m["c"]["ci"] == [0.0, 0.0]
      and abs(m["b"]["score"] - np.mean([q[d]["b"]["score"] for d in q])) < 1e-12)
check("script share: Hindi text is Devanagari, English is not, Meitei is Meetei Mayek",
      ev.script_share(TEXT["hin"], "Deva") == 1.0 and ev.script_share(TEXT["eng"], "Deva") == 0.0
      and ev.script_share(TEXT["mni"], "Mtei") == 1.0)

# 7. IndicTrans2's own code (transformers 4) in its venv, on a tiny random model of its architecture
it2 = ev.ROOT / ".venv-it2/bin/python"
if it2.exists():
    r = subprocess.run([str(it2), str(Path(__file__).with_name("test_indictrans_remote.py"))], capture_output=True,
                       text=True)
    lines = [l for l in r.stdout.splitlines() if l.startswith(("PASS", "FAIL", "SKIP"))]
    print("\n".join(lines))
    results += [l.startswith("PASS") for l in lines] + [r.returncode == 0]
else:
    print(f"SKIP  IndicTrans2's remote code: no {it2} (README: the IndicTrans2 environment)")

tmp.cleanup()
print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
