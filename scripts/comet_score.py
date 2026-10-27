import argparse
import importlib.metadata
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_translate import CONFIGS, DATA, ROOT, RUNS, append_jsonl, load_data, read_jsonl, repair_jsonl, sha256

COMET = dict(repo="Unbabel/wmt22-comet-da", revision="2760a223ac957f30acfb18c8aa649b01cf1d75f2",
             sha256="e213091cde220f97b89f8bdfa750c458cfea741ad62affb455b59900210ff2af",
             encoder="FacebookAI/xlm-roberta-large", encoder_revision="c23d21b0620b635a76227c604d44e43a9f0ee389")
MODEL, ENCODER = ROOT / "data/models/wmt22-comet-da", ROOT / "data/models/xlm-roberta-large"


def load_model():
    """wmt22-comet-da on the CPU, its encoder's config and tokenizer from the local copy (the checkpoint holds every
    weight; comet.load_from_checkpoint would look the encoder up on the Hub by name)."""
    import torch
    import yaml
    from comet.models import str2model
    ckpt = MODEL / "checkpoints/model.ckpt"
    if not ckpt.exists() or sha256(ckpt) != COMET["sha256"]:
        sys.exit(f"{ckpt}: missing or not the pinned checkpoint (requirements-comet.txt says how to fetch it)")
    hp = yaml.safe_load(open(MODEL / "hparams.yaml"))
    return str2model[hp["class_identifier"]].load_from_checkpoint(
        checkpoint_path=ckpt, load_pretrained_weights=False, map_location=torch.device("cpu"), strict=False,
        pretrained_model=str(ENCODER)).eval()


def identity() -> dict:
    return dict(COMET, package=importlib.metadata.version("unbabel-comet"), scale="segment score x 100")


def score_run(model, run: Path, items: dict, batch: int, chunk: int, log) -> int:
    """Every generated output of a run -> run/comet/{direction}.jsonl ({id, comet}); resumes per item. Directions go
    to the model `chunk` outputs at a time (each predict call has a fixed cost) and are written whole."""
    meta = run / "comet.json"
    if meta.exists() and json.load(open(meta)) != identity():
        sys.exit(f"{meta}: COMET scores of another model or package; move {run / 'comet'} away first")
    meta.write_text(json.dumps(identity(), indent=1))
    todo = []
    for gen in sorted((run / "gen").glob("*.jsonl")):
        out = run / "comet" / gen.name
        if out.exists():
            repair_jsonl(out)
        done = {r["id"] for r in read_jsonl(out)}
        if recs := [r for r in read_jsonl(gen) if r["id"] not in done]:
            todo.append((gen.stem, out, recs))
    made = 0
    while todo:
        group, n = [], 0
        while todo and (not group or n + len(todo[0][2]) <= chunk):
            group.append(todo.pop(0))
            n += len(group[-1][2])
        data = [dict(src=items[r["id"]]["text"][src], mt=r["hyp"], ref=items[r["id"]]["text"][tgt])
                for d, _, recs in group for src, tgt in [d.split("-")] for r in recs]
        scores = iter(model.predict(data, batch_size=batch, gpus=0, progress_bar=False, num_workers=1).scores)
        for _, out, recs in group:
            for r in recs:
                append_jsonl(out, dict(id=r["id"], comet=100 * float(next(scores))))
        made += n
        log(f"{run.name} {group[0][0]}..{group[-1][0]}: {n} outputs")
    return made


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("configs", nargs="+", help=f"run directories under --runs (configs: {', '.join(CONFIGS)})")
    ap.add_argument("--data", default=str(DATA))
    ap.add_argument("--runs", default=str(RUNS))
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--chunk", type=int, default=600, help="outputs per predict call")
    a = ap.parse_args()
    items, _ = load_data(a.data)
    if missing := [c for c in a.configs if not (Path(a.runs) / c / "gen").is_dir()]:
        sys.exit(f"no outputs for {', '.join(missing)} in {a.runs}")
    import torch
    torch.set_grad_enabled(False)
    model, t0 = load_model(), time.perf_counter()
    log = lambda m: print(f"{m} [{time.perf_counter() - t0:.0f} s]", flush=True)
    for c in a.configs:
        log(f"{c}: {score_run(model, Path(a.runs) / c, items, a.batch, a.chunk, log)} outputs scored")


if __name__ == "__main__":
    main()
