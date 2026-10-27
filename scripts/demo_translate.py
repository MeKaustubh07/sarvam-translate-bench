import argparse
import json
import os
import sys
import time
from pathlib import Path

import httpx

ENGINE = Path(os.environ.get("ENGINE", Path(__file__).resolve().parent.parent.parent / "InferenceEngine")).resolve()
sys.path.insert(0, str(ENGINE / "src"))
from tokenizer import Tokenizer

LANGUAGES = {"hin": "Hindi", "mni": "Manipuri", "sat": "Santali", "mar": "Marathi", "tam": "Tamil", "ben": "Bengali",
             "urd": "Urdu", "kan": "Kannada", "guj": "Gujarati", "pan": "Punjabi", "mal": "Malayalam", "ory": "Odia"}
COLOURS = ["\033[38;5;214m", "\033[38;5;81m", "\033[38;5;120m", "\033[38;5;213m", "\033[38;5;227m"]
DIM, BOLD, RESET = "\033[2m", "\033[1m", "\033[0m"
TEXT = "Every child in the village can now learn in their own language."


def translate(client: httpx.Client, url: str, text: str, language: str, colour: str, tok: Tokenizer) -> None:
    body = {"messages": [{"role": "system", "content": f"Translate the text below to {language}."},
                         {"role": "user", "content": text}], "stream": True, "temperature": 0}
    print(f"{BOLD}{colour}{language}{RESET}  ", end="", flush=True)
    out, start, first = [], time.perf_counter(), None
    with client.stream("POST", f"{url}/v1/chat/completions", json=body) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line.startswith("data: ") or line == "data: [DONE]":
                continue
            msg = json.loads(line[6:])
            if "error" in msg:
                sys.exit(msg["error"]["message"])
            if piece := msg["choices"][0].get("delta", {}).get("content"):
                first = first or time.perf_counter()
                out.append(piece)
                print(f"{colour}{piece}{RESET}", end="", flush=True)
    secs, text_out = time.perf_counter() - (first or start), "".join(out)
    tokens = len(tok.encode(text_out))
    print(f"\n{DIM}  {tokens} tokens · {tokens / secs:.1f} tok/s · {len(text_out) / secs:.0f} chars/s · "
          f"first token {(first or start) - start:.2f} s{RESET}\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("text", nargs="?", default=TEXT)
    ap.add_argument("--to", default="hin,mni,sat", help=f"comma-separated codes: {', '.join(LANGUAGES)}")
    ap.add_argument("--url", default="http://127.0.0.1:8000")
    a = ap.parse_args()
    tok = Tokenizer(str(ENGINE / "models/sarvam-translate/tokenizer.json"))
    print(f"{BOLD}English{RESET}  {a.text}\n")
    with httpx.Client(timeout=None) as client:
        try:
            client.get(f"{a.url}/health").raise_for_status()
        except httpx.HTTPError:
            sys.exit(f"no server at {a.url}: start {ENGINE}/scripts/serve.py --model sarvam-translate --backend metal-int4")
        for i, code in enumerate(a.to.split(",")):
            translate(client, a.url, a.text, LANGUAGES[code], COLOURS[i % len(COLOURS)], tok)


if __name__ == "__main__":
    main()
