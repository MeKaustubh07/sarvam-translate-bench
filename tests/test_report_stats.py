import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

from bench_fixtures import check, finish, in22_rows
import numpy as np

import eval_translate_report as report
from sacrebleu.metrics import CHRF

# the protocol on canonically equal text, chrF++ against sacrebleu's CLI, the paired and the macro bootstrap
chrf, rows = CHRF(word_order=2), in22_rows()
tmp = tempfile.TemporaryDirectory()
T = Path(tmp.name)
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
    ref = rows[k]["sentence_hin_Deva" if k % 2 else "sentence_eng_Latn"]
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

tmp.cleanup()
finish()
