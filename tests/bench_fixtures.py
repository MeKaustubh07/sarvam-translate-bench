import os
import sys
import unicodedata
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import eval_translate as ev

results = []
def check(name, ok):
    results.append(bool(ok)); print(f"{'PASS' if ok else 'FAIL'}  {name}", flush=True)


def refused(fn):
    try:
        fn(); return False
    except SystemExit:
        return True


def finish() -> None:
    print(f"\n{sum(results)}/{len(results)} passed")
    sys.exit(0 if all(results) else 1)


# synthetic text: English words, and the same words spelled letter for letter in each language's script
def letters(script: str) -> list[str]:
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


def in22_rows() -> list[dict]:
    """104 IN22-Gen-shaped rows (13 domains x 2 sources x 4), ids from 1, a column per language in its script."""
    rng, rows = np.random.default_rng(0), []
    for k in range(104):
        en = " ".join(rng.choice(WORDS, size=int(rng.integers(3, 6)))).capitalize() + "."
        row = dict(id=k + 1, context="ctx", source=("web", "wikipedia")[k % 2], url="", domain=DOMAINS[k // 2 % 13],
                   num_words=len(en.split()), bucket="1 - 10")
        for code in ev.NAMES:
            script = SCRIPT_OF.get(code, "Deva")
            row[f"sentence_{code}_{script}"] = en if code == "eng" else spell(en.lower(), script)
        row["sentence_mni_Beng"] = spell(en.lower(), "Beng")   # a second script for Manipuri: Meitei is picked
        rows.append(row)
    return rows
