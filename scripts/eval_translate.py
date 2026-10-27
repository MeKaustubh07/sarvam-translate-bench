import argparse
import hashlib
import importlib.util
import json
import os
import random
import re
import subprocess
import sys
import types
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE = Path(os.environ.get("ENGINE", ROOT.parent / "InferenceEngine")).resolve()
sys.path[:0] = [str(ROOT / "scripts"), str(ENGINE / "src")]

IN22 = dict(repo="ai4bharat/IN22-Gen", revision="e042ab3d3063110b1a85efa0a59bdbf8553bb928",
            file="data/train-00000-of-00001.parquet",
            sha256="e79c7889abe97c78cf03c09f04e50874b7932b381b49a08a4431e58aefc5fb5c")
DATA, RUNS, OUT = ROOT / "data/in22-gen", ROOT / "runs", ROOT / "results"
ENG = "eng"
NAMES = {"eng": "English", "asm": "Assamese", "ben": "Bengali", "brx": "Bodo", "doi": "Dogri", "gom": "Konkani",
         "guj": "Gujarati", "hin": "Hindi", "kan": "Kannada", "kas": "Kashmiri", "mai": "Maithili", "mal": "Malayalam",
         "mar": "Marathi", "mni": "Manipuri", "npi": "Nepali", "ory": "Odia", "pan": "Punjabi", "san": "Sanskrit",
         "sat": "Santali", "snd": "Sindhi", "tam": "Tamil", "tel": "Telugu", "urd": "Urdu"}
LANGS = [c for c in NAMES if c != ENG]
SCRIPT_PREF = {"mni": ("Mtei", "Meitei Mayek"), "snd": ("Deva", "Devanagari"), "kas": ("Arab", "Perso-Arabic"),
               "sat": ("Olck", "Ol Chiki")}    # written in more than one script: IN22-Gen's column, named in the prompt
SCRIPTS = {"Latn": "LATIN", "Deva": "DEVANAGARI", "Beng": "BENGALI", "Guru": "GURMUKHI", "Gujr": "GUJARATI",
           "Orya": "ORIYA", "Taml": "TAMIL", "Telu": "TELUGU", "Knda": "KANNADA", "Mlym": "MALAYALAM",
           "Arab": "ARABIC", "Mtei": "MEETEI MAYEK", "Olck": "OL CHIKI"}           # Unicode name prefixes
LANG_COL = re.compile(r"(?:sentence_)?([a-z]{3})_([A-Z][a-z]{3})")
META, STRATA = ("id", "domain", "source", "bucket", "num_words"), ("domain", "source")
CONFIGS = {   # name: (the engine's registry model or indictrans.HF, backend, INT4 policy: "calibrated" | "flat" | None)
    "sarvam-int8": ("sarvam-translate", "metal-int8", None),
    "sarvam-int4": ("sarvam-translate", "metal-int4", "calibrated"),
    "gemma-int8": ("gemma-3-4b-it", "metal-int8", None),
    "gemma-int4": ("gemma-3-4b-it", "metal-int4", "calibrated"),
    "indictrans2": ("indictrans2", "hf", None),
    "indictrans2-beam5": ("indictrans2-beam5", "hf", None)}                   # a control: the paper's beam 5
QT_NAME = {None: "model.int8.qt", "calibrated": "model.int4.qt", "flat": "model.int4-flat.qt"}   # by policy
SUPPORT = {"sarvam-translate": set(NAMES), "indictrans2": set(NAMES)}   # the cards' lists; Gemma 3: 140, no list
MAX_NEW = [32, 4.0]


def sha256(path) -> str:
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def script_share(text: str, script: str) -> float:
    """Of the letters and marks in text, the share in `script` (1.0 for no letters)."""
    letters = [c for c in text if unicodedata.category(c)[0] in "LM"]
    return sum(unicodedata.name(c, "").startswith(SCRIPTS[script]) for c in letters) / len(letters) if letters else 1.0


def read_jsonl(path: Path) -> list[dict]:
    """A results file's complete records: a last line without its newline (being written, or torn) is skipped."""
    if not path.exists():
        return []
    raw = path.read_bytes()
    return [json.loads(line) for line in raw[:raw.rfind(b"\n") + 1].decode("utf-8").splitlines() if line]


def repair_jsonl(path: Path) -> None:
    """Cut a torn last line (the writer died mid-line) so appends stay clean; only the writer calls this."""
    if (raw := path.read_bytes()) and not raw.endswith(b"\n"):
        os.truncate(path, raw.rfind(b"\n") + 1)


def import_without_init(package: str) -> None:
    """Register an installed package without running its __init__, whose imports the parts used here do not need (and
    which fail on this stack), so that its submodules import."""
    if package not in sys.modules:
        pkg = types.ModuleType(package)
        pkg.__path__ = list(importlib.util.find_spec(package).submodule_search_locations)
        sys.modules[package] = pkg


def append_jsonl(path: Path, rec: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


# --- data ---------------------------------------------------------------------------------------------------------

def write_dataset(rows: list[dict], out: Path, source: dict) -> dict:
    """IN22-Gen rows (a column per language) -> out/in22_gen.jsonl ({id, domain, ..., text: {639-3 code: text}}, texts
    trimmed) and out/manifest.json (each language's column, its script checked on the text, SHA-256s, strata)."""
    if "id" not in rows[0]:                            # IN22-Gen has none: the row's place in the pinned parquet
        rows = [{"id": i} | r for i, r in enumerate(rows)]
    cols ={m.group(1, 2): c for c in rows[0] if (m := LANG_COL.fullmatch(c))}
    langs = {}
    for code in NAMES:
        if not (scripts := [s for (lang, s) in cols if lang == code]):
            raise ValueError(f"no {code} column among {sorted(rows[0])}")
        pick = SCRIPT_PREF[code][0] if code in SCRIPT_PREF else scripts[0]
        if pick not in scripts or (len(scripts) > 1 and code not in SCRIPT_PREF):
            raise ValueError(f"{code}: columns in {scripts}, the prompts name {pick}: set SCRIPT_PREF")
        texts = [(r[cols[code, pick]] or "").strip() for r in rows]
        langs[code] = dict(column=cols[code, pick], script=pick, other_scripts=sorted(set(scripts) - {pick}),
                           script_share=round(script_share(" ".join(texts), pick), 4), empty=texts.count(""))
    items = [{k: r[k] for k in META if k in r} | {"text": {c: (r[v["column"]] or "").strip()
                                                           for c, v in langs.items()}} for r in rows]
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "in22_gen.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(it, ensure_ascii=False) + "\n" for it in items)
    strata = Counter("/".join(str(it.get(s)) for s in STRATA) for it in items)
    manifest = dict(source=source, rows=len(items), columns=list(rows[0]), languages=langs, strata=dict(sorted(
        strata.items())), jsonl="in22_gen.jsonl", jsonl_sha256=sha256(out / "in22_gen.jsonl"))
    json.dump(manifest, open(out / "manifest.json", "w"), indent=1)
    return manifest


def cmd_data(a) -> None:
    from huggingface_hub import hf_hub_download
    from huggingface_hub.errors import GatedRepoError
    try:
        path = hf_hub_download(IN22["repo"], IN22["file"], repo_type="dataset", revision=IN22["revision"],
                               local_dir=a.data)
    except GatedRepoError:
        sys.exit(f"{IN22['repo']} is gated: accept its terms at https://huggingface.co/datasets/{IN22['repo']} "
                 "(approved automatically) with the account of your HF token, then rerun")
    if (got := sha256(path)) != IN22["sha256"]:
        sys.exit(f"{path}: SHA-256 {got}, pinned {IN22['sha256']}")
    import pyarrow.parquet as pq
    m = write_dataset(pq.read_table(path).to_pylist(), Path(a.data), IN22)
    print(json.dumps(m["languages"], indent=1) + f"\n{m['rows']} rows, strata {m['strata']}\nwrote {a.data}/"
          f"in22_gen.jsonl (sha256 {m['jsonl_sha256']}) and manifest.json")


def load_data(data: str) -> tuple[dict[int, dict], dict]:
    d = Path(data)
    if not (d / "manifest.json").exists():
        sys.exit(f"no dataset in {d}: run `eval_translate.py data` first")
    manifest = json.load(open(d / "manifest.json"))
    if sha256(d / manifest["jsonl"]) != manifest["jsonl_sha256"]:
        sys.exit(f"{d / manifest['jsonl']} does not match its manifest's SHA-256")
    return {it["id"]: it for it in read_jsonl(d / manifest["jsonl"])}, manifest


def sample_ids(items: dict[int, dict], n: int, seed: int) -> list[int]:
    """The first n of one seeded order of the ids in which every stratum is spread evenly:
    each stratum's ids, shuffled, at evenly spaced keys in [0, 1) from a random offset."""
    rng, cells, keyed = random.Random(seed), defaultdict(list), []
    for i, it in sorted(items.items()):
        cells[tuple(str(it.get(s)) for s in STRATA)].append(i)
    for key in sorted(cells):
        rng.shuffle(ids := cells[key])
        u = rng.random()
        keyed += [((k + u) / len(ids), key, i) for k, i in enumerate(ids)]
    return [i for *_, i in sorted(keyed)][:n]


def pairs(items: dict, ids: list[int], langs: list[str], done_in):
    """-> (src, tgt, path, ids to do) per direction, English -> X first; done_in(src, tgt) -> (path, ids done).
    Items without text on both sides are skipped (the manifest counts empty texts)."""
    for src, tgt in [(ENG, x) for x in langs] + [(x, ENG) for x in langs]:
        path, done = done_in(src, tgt)
        yield src, tgt, path, [i for i in ids if i not in done and items[i]["text"][src] and items[i]["text"][tgt]]


# --- models -------------------------------------------------------------------------------------------------------

def label(code: str) -> str:
    return f"{NAMES[code]} ({SCRIPT_PREF[code][1]} script)" if code in SCRIPT_PREF else NAMES[code]


def messages(style: str, source: str, target: str, text: str) -> list[dict]:
    """The chat for one translation; style "card" (Sarvam-Translate's, given to Gemma 3 too: an ablation of the
    fine-tune) or "neutral" (a control); source / target: language names."""
    if style == "card":
        return [{"role": "system", "content": f"Translate the text below to {target}."},
                {"role": "user", "content": text}]
    return [{"role": "user", "content": f"Translate the following text from {source} to {target}. Reply with the "
                                        f"translation only.\n\n{text}"}]


def prompt(eng, src: str, tgt: str, text: str, style: str | None = None) -> str:
    """The rendered prompt (the template writes BOS; Gemma 3's folds the system turn into the user's). The card's
    prompt names the target as the card does; the neutral one adds the script where there is a choice."""
    from chat import format_chat
    style = style or "card"
    names = (NAMES[src], NAMES[tgt]) if style == "card" else (label(src), label(tgt))
    return format_chat(messages(style, *names, text), style=eng.chat_style, enable_thinking=False)


def code_version(engine: bool = True) -> dict:
    """What made a run segment: git describe of this repo (and the engine's), and a SHA-256 of the code that makes the
    outputs (this script, and the engine's src/ or the seq2seq backend)."""
    def describe(repo: Path) -> str:
        git = subprocess.run(["git", "describe", "--always", "--dirty"], cwd=repo, capture_output=True, text=True)
        return git.stdout.strip() or "uncommitted"
    here = Path(__file__).resolve()
    files = [(ROOT, here)] + ([(ROOT, here.with_name("engine_run.py"))] + [
        (ENGINE, f) for f in sorted((ENGINE / "src").rglob("*.py"))] if engine else [(ROOT, here.with_name("indictrans.py"))])
    h = hashlib.sha256()
    for root, f in files:
        h.update(str(f.relative_to(root)).encode() + b"\0" + f.read_bytes())
    git = f"{describe(ROOT)}" + (f" engine {describe(ENGINE)}" if engine else "")
    return dict(git=git, code_sha256=h.hexdigest()[:16])


def open_dir(a, kind: str, identity: dict):
    """-> (run directory, (src, tgt) -> (results file, ids done)). Results of another identity in the directory are
    refused; torn lines are cut."""
    run = Path(a.runs) / (a.config + (f"@{a.prompt}" if getattr(a, "prompt", None) not in (None, "card") else ""))
    run.mkdir(parents=True, exist_ok=True)
    if (meta := run / "meta.json").exists() and (old := json.load(open(meta))) != identity:
        diff = {k: old.get(k) for k in identity if old.get(k) != identity[k]}
        sys.exit(f"{run} holds results of another build ({diff}); move it away first")
    json.dump(identity, open(meta, "w"), indent=1, ensure_ascii=False)
    for f in run.rglob("*.jsonl"):
        repair_jsonl(f)

    def done_in(src, tgt):
        path = run / kind / f"{src}-{tgt}.jsonl"
        return path, {r["id"] for r in read_jsonl(path)}
    return run, done_in


def footprint_peak_mib() -> float:
    """This process's lifetime peak physical footprint (MiB), CPU and Metal memory alike, as the engine's
    scripts/bench.py footprint_mib reads it (macOS proc_pid_rusage, RUSAGE_INFO_V4: lifetime_max_phys_footprint)."""
    import ctypes
    buf = (ctypes.c_uint64 * 64)()
    if ctypes.CDLL("/usr/lib/libproc.dylib").proc_pid_rusage(os.getpid(), 4, buf) != 0:
        return float("nan")
    return buf[2 + 28] / 2**20


def gpu_peak_bytes(device) -> int | None:
    """The allocator's peak + what Metal holds outside it now (tests/serving_targets.py gpu_peak); None off the GPU."""
    import torch
    if device.type != "mps":
        return None
    torch.mps.synchronize()
    A = torch.accelerator
    return A.max_memory_reserved() + max(0, torch.mps.driver_allocated_memory() - A.memory_reserved())


def cmd_generate(a) -> None:
    from engine_run import generate as engine_generate
    from indictrans import generate as hf_generate
    (hf_generate if CONFIGS[a.config][1] == "hf" else engine_generate)(a)


def cmd_score(a) -> None:
    from engine_run import score as engine_score
    from indictrans import score as hf_score
    (hf_score if CONFIGS[a.config][1] == "hf" else engine_score)(a)


def main(argv=None) -> None:
    split = lambda s: s.split(",")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--data", default=str(DATA))
    common.add_argument("--runs", default=str(RUNS))
    common.add_argument("--seed", type=int, default=0)
    model = argparse.ArgumentParser(add_help=False, parents=[common])
    model.add_argument("config", choices=list(CONFIGS))
    model.add_argument("--langs", type=split, default=LANGS)
    model.add_argument("--weights", help="a .qt file in place of the model's own")
    model.add_argument("--prompt", choices=("card", "neutral"), help="engine configs, a control: another prompt than "
                       "the card's")
    model.add_argument("--device", default="mps", help="hf configs: the torch device")
    model.add_argument("--dtype", choices=("float32", "float16", "bfloat16"), default="float16",
                       help="hf configs: the weights' and activations' dtype (`parity` measures it)")
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("data", parents=[common])
    gen = sub.add_parser("generate", parents=[model])
    gen.add_argument("--n", type=int, default=50)
    gen.add_argument("--batch", type=int, default=8)
    gen.add_argument("--kv-blocks", type=int, default=384)
    gen.add_argument("--no-prefix-cache", action="store_true")
    sc = sub.add_parser("score", parents=[model])
    sc.add_argument("--n", type=int, default=200)
    sc.add_argument("--batch", type=int, default=8, help="hf configs: references per forward")
    par = sub.add_parser("parity", parents=[common], help="indictrans2 on --device / --dtype vs CPU float32")
    par.add_argument("--device", default="mps")
    par.add_argument("--dtype", choices=("float16", "bfloat16"), default="float16")
    par.add_argument("--n", type=int, default=8, help="ids per direction")
    par.add_argument("--langs", type=split, default=["hin", "tam", "mni", "urd"])
    rep = sub.add_parser("report", parents=[common])
    rep.add_argument("--configs", type=split)
    rep.add_argument("--baseline", help="the config deltas are taken against (default sarvam-int4)")
    rep.add_argument("--boot", type=int, default=1000)
    rep.add_argument("--out", default=str(OUT))
    a = ap.parse_args(argv)
    if bad := set(getattr(a, "langs", ())) - set(LANGS):
        ap.error(f"unknown languages {sorted(bad)}; known: {','.join(LANGS)}")
    if a.cmd == "report":
        from eval_translate_report import cmd_report
        return cmd_report(a)
    if a.cmd == "parity":
        from indictrans import parity
        return parity(a)
    {"data": cmd_data, "generate": cmd_generate, "score": cmd_score}[a.cmd](a)


if __name__ == "__main__":
    main()
