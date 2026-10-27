import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import eval_translate as ev
import indictrans

torch.set_grad_enabled(False)
results = []
def check(name, ok):
    results.append(bool(ok)); print(f"{'PASS' if ok else 'FAIL'}  {name}", flush=True)


# IndicTrans2's own tokenizer and model code (transformers 4, .venv-it2) on a tiny random model of its architecture:
# the small files of both checkpoints and the IN22-Gen data are read, the weights never
dirs = {side: ev.ROOT / d for side, d in indictrans.HF["indictrans2"].items()}
need = [d / f for d in dirs.values() for f in ("config.json", "modeling_indictrans.py", "tokenization_indictrans.py",
                                               "dict.SRC.json", "dict.TGT.json", "model.SRC", "model.TGT")]
if not all(f.exists() for f in need) or not (ev.DATA / "manifest.json").exists():
    print(f"SKIP: needs IndicTrans2's small files in {', '.join(map(str, dirs.values()))} and the data in {ev.DATA}")
    sys.exit(0)
from transformers import AutoConfig, AutoModelForSeq2SeqLM, AutoTokenizer

items, man = ev.load_data(str(ev.DATA))
ids = ev.sample_ids(items, 20, 0)
ip = indictrans.processor(False)
T = Path(tempfile.mkdtemp())
for side, d in dirs.items():
    tok = AutoTokenizer.from_pretrained(d, trust_remote_code=True)
    src_vocab = json.load(open(d / "dict.SRC.json"))
    tags = {indictrans.flores(x, man) for x in ev.NAMES}
    langs = ev.LANGS if side == "en-x" else [ev.ENG]
    same, n = 0, 0
    for x in langs:
        text = ip.preprocess_batch([items[i]["text"][x] for i in ids], src_lang=indictrans.flores(x, man), is_target=True)
        enc = tok(text_target=text, add_special_tokens=False)["input_ids"]
        same += sum(tok.decode(e, clean_up_tokenization_spaces=False) == t for e, t in zip(enc, text))
        n += len(text)
    src = tok(["eng_Latn mni_Mtei A test ." if side == "en-x" else "mni_Mtei eng_Latn ꯑ ."])["input_ids"][0]
    check(f"{side} tokenizer: every IN22-Gen tag is one source token; a source starts with its two tags and ends with "
          f"</s>; pre-processed references decode back to their text ({same}/{n}, at least 90%: SentencePiece normalises some, e.g. Odia nukta letters)",
          tags <= set(src_vocab) and src[-1] == tok.eos_token_id == 2 and tok.decode([]) == ""
          and src[:2] == [src_vocab[t] for t in (("eng_Latn", "mni_Mtei") if side == "en-x" else ("mni_Mtei", "eng_Latn"))]
          and same >= 0.9 * n)

    # a tiny model of the real architecture and vocabularies, saved beside the real code and tokenizer files
    t = T / d.name
    t.mkdir()
    for f in d.iterdir():
        if f.is_file() and f.suffix not in (".safetensors", ".bin"):
            shutil.copy(f, t)
    cfg = AutoConfig.from_pretrained(d, trust_remote_code=True)
    for k, v in dict(encoder_layers=2, decoder_layers=2, encoder_embed_dim=64, decoder_embed_dim=64, encoder_ffn_dim=128,
                     decoder_ffn_dim=128, encoder_attention_heads=4, decoder_attention_heads=4, init_std=0.5).items():
        setattr(cfg, k, v)
    torch.manual_seed(0)
    AutoModelForSeq2SeqLM.from_config(cfg, trust_remote_code=True).save_pretrained(t)
    indictrans.HF.setdefault("tiny-real", {})[side] = str(t)
ev.CONFIGS["tiny-real"] = ("tiny-real", "hf", None)
R = T / "runs"
COMMON = ["--runs", str(R), "--langs", "hin,mni,urd", "--n", "4", "--batch", "3", "--device", "cpu", "--dtype", "float32"]
ev.main(["generate", "tiny-real", *COMMON])
ev.main(["score", "tiny-real", *COMMON])
gen = {f.stem: ev.read_jsonl(f) for f in sorted((R / "tiny-real/gen").glob("*.jsonl"))}
sc = {f.stem: ev.read_jsonl(f) for f in sorted((R / "tiny-real/score").glob("*.jsonl"))}
s2s, gp = indictrans.Seq2Seq("tiny-real", "cpu", "float32"), indictrans.processor(True)
same, worst = True, 0.0
for k in gen:
    src, tgt = k.split("-")
    model, tok = s2s.load(src)
    sl, tl = indictrans.flores(src, man), indictrans.flores(tgt, man)
    for r in gen[k]:                                       # alone, without the cache: the whole prefix each step
        text = items[r["id"]]["text"][src]
        x = tok(gp.preprocess_batch([text], src_lang=sl, tgt_lang=tl), return_tensors="pt")["input_ids"]
        cap, out, cur = ev.MAX_NEW[0] + int(np.ceil(ev.MAX_NEW[1] * len(text))), [], torch.tensor([[2]])
        while len(out) < min(cap, model.config.max_target_positions - 1):
            nxt = int(model(input_ids=x, decoder_input_ids=cur).logits[0, -1].argmax())
            if nxt == 2:
                break
            out.append(nxt)
            cur = torch.cat([cur, torch.tensor([[nxt]])], 1)
        hyp = gp.postprocess_batch([tok.decode(out, skip_special_tokens=True, clean_up_tokenization_spaces=True)],
                                   lang=tl)[0].strip()
        same &= len(out) == r["tokens"] and hyp == r["hyp"]
    for r in sc[k]:
        x = tok(ip.preprocess_batch([items[r["id"]]["text"][src]], src_lang=sl, tgt_lang=tl), return_tensors="pt")
        ref = ip.preprocess_batch([items[r["id"]]["text"][tgt]], src_lang=tl, is_target=True)
        lab = tok(text_target=ref, add_special_tokens=False)["input_ids"][0] + [2]
        lp = torch.log_softmax(model(**x, decoder_input_ids=torch.tensor([[2] + lab[:-1]])).logits[0].double(), -1)
        nll = -lp[torch.arange(len(lab)), torch.tensor(lab)]
        worst = max(worst, abs(r["nats"] - nll[:-1].sum().item()) / nll[:-1].sum().item(),
                    abs(r["end_nats"] - nll[-1].item()) / nll[-1].item())
check(f"tiny IndicTrans (its remote code): generate and score over 6 directions x 4 ids; batched greedy with the "
      f"legacy KV cache == one source at a time without it (tokens, post-processed text); nats == one unpadded forward "
      f"(worst rel {worst:.1e} < 1e-5)", len(gen) == len(sc) == 6 and all(len(v) == 4 for v in gen.values())
      and all(len(v) == 4 for v in sc.values()) and same and worst < 1e-5)
shutil.rmtree(T)
print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
