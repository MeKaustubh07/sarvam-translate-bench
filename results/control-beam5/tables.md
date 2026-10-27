chrF++: sacrebleu `nrefs:1|case:mixed|eff:yes|nc:6|nw:2|space:no|version:2.6.0`, corpus level over the sampled ids, on IN22's protocol (IN22-Gen / IndicTrans2 compute_metrics.sh: Indic targets IndicNLP normalize (default options) + trivial_tokenize, English raw; indic-nlp-library 0.92, urduhack 1.1.1). In brackets: the difference from indictrans2 and its paired bootstrap 95% CI (1000 resamples, seed 0; a macro row resamples the shared ids jointly over its languages). Support claimed by indictrans2 / indictrans2-beam5. Macro rows: all languages; one script (without Manipuri, Sindhi, Kashmiri, Santali, written in more than one); a config without every language of a row shows -.

COMET: Unbabel/wmt22-comet-da (revision 2760a223, unbabel-comet 2.2.7), reference-based, raw text (no IN22 normalisation), on the CPU. Its encoder (XLM-R) never saw Bodo, Dogri, Konkani, Kashmiri, Maithili, Manipuri, Santali, Sindhi: their COMET is not reliable; the macro over XLM-R's languages leaves them out.

Bits per character compare models that score the reference itself: none. indictrans2 score IndicProcessor's pre-processed reference, reported apart.

### chrF++ (higher is better), English -> X

| language | support | n | indictrans2 | indictrans2-beam5 |
|---|---:|---:|---:|---:|
| Assamese | yes / ? | 10 | 47.0 | 48.6 (+1.6 [-0.5, +6.4]) |
| Bengali | yes / ? | 10 | 56.6 | 57.0 (+0.4 [-0.4, +1.7]) |
| Bodo | yes / ? | 10 | 48.4 | 49.2 (+0.8 [-0.9, +2.4]) |
| Dogri | yes / ? | 10 | 56.1 | 56.5 (+0.4 [-1.2, +1.9]) |
| Konkani | yes / ? | 10 | 46.2 | 45.3 (-0.8 [-3.2, +0.9]) |
| Gujarati | yes / ? | 10 | 57.3 | 59.2 (+2.0 [+0.1, +5.1]) |
| Hindi | yes / ? | 10 | 59.1 | 60.0 (+0.9 [-2.3, +6.2]) |
| Kannada | yes / ? | 10 | 55.8 | 54.7 (-1.1 [-3.1, +1.2]) |
| Kashmiri | yes / ? | 10 | 41.3 | 40.6 (-0.7 [-1.5, +0.2]) |
| Maithili | yes / ? | 10 | 53.3 | 52.3 (-1.0 [-3.5, +1.7]) |
| Malayalam | yes / ? | 10 | 60.0 | 60.4 (+0.4 [-1.4, +2.9]) |
| Marathi | yes / ? | 10 | 55.8 | 55.9 (+0.1 [-1.0, +1.5]) |
| Manipuri | yes / ? | 10 | 48.7 | 50.3 (+1.6 [-0.3, +3.1]) |
| Nepali | yes / ? | 10 | 54.2 | 54.5 (+0.3 [-0.0, +0.8]) |
| Odia | yes / ? | 10 | 42.2 | 41.9 (-0.3 [-1.5, +0.7]) |
| Punjabi | yes / ? | 10 | 51.3 | 51.8 (+0.4 [-0.5, +1.4]) |
| Sanskrit | yes / ? | 10 | 38.8 | 39.9 (+1.1 [-1.3, +5.6]) |
| Santali | yes / ? | 10 | 36.0 | 37.2 (+1.2 [-0.1, +2.6]) |
| Sindhi | yes / ? | 10 | 34.1 | 35.0 (+0.9 [-2.3, +5.4]) |
| Tamil | yes / ? | 10 | 48.6 | 51.0 (+2.3 [+0.1, +4.1]) |
| Telugu | yes / ? | 10 | 60.7 | 60.0 (-0.7 [-1.7, +0.0]) |
| Urdu | yes / ? | 10 | 70.9 | 75.1 (+4.2 [+1.7, +6.6]) |
| **macro, all (22)** |  | 10 | 51.0 | 51.7 (+0.6 [+0.2, +1.5]) |
| **macro, one script (18)** |  | 10 | 53.5 | 54.1 (+0.6 [+0.1, +1.6]) |

### chrF++ (higher is better), X -> English

| language | support | n | indictrans2 | indictrans2-beam5 |
|---|---:|---:|---:|---:|
| Assamese | yes / ? | 10 | 64.7 | 66.2 (+1.5 [-0.0, +4.0]) |
| Bengali | yes / ? | 10 | 66.7 | 67.3 (+0.6 [-3.2, +5.0]) |
| Bodo | yes / ? | 10 | 65.8 | 65.5 (-0.3 [-3.9, +2.7]) |
| Dogri | yes / ? | 10 | 78.0 | 79.8 (+1.8 [+0.1, +3.6]) |
| Konkani | yes / ? | 10 | 64.4 | 64.7 (+0.3 [-1.4, +1.3]) |
| Gujarati | yes / ? | 10 | 73.9 | 72.8 (-1.1 [-5.4, +2.0]) |
| Hindi | yes / ? | 10 | 66.7 | 66.8 (+0.0 [-2.9, +2.1]) |
| Kannada | yes / ? | 10 | 71.6 | 69.5 (-2.1 [-6.3, +0.6]) |
| Kashmiri | yes / ? | 10 | 59.4 | 58.4 (-1.0 [-2.2, +0.1]) |
| Maithili | yes / ? | 10 | 76.4 | 78.2 (+1.8 [+0.4, +3.8]) |
| Malayalam | yes / ? | 10 | 70.2 | 72.4 (+2.2 [+0.5, +4.6]) |
| Marathi | yes / ? | 10 | 68.9 | 69.6 (+0.7 [-1.0, +2.4]) |
| Manipuri | yes / ? | 10 | 62.5 | 64.8 (+2.4 [-1.3, +5.7]) |
| Nepali | yes / ? | 10 | 76.2 | 74.8 (-1.4 [-3.2, -0.2]) |
| Odia | yes / ? | 10 | 69.3 | 69.9 (+0.5 [-1.4, +3.5]) |
| Punjabi | yes / ? | 10 | 68.0 | 66.7 (-1.2 [-2.4, +0.2]) |
| Sanskrit | yes / ? | 10 | 57.3 | 59.7 (+2.4 [-0.5, +6.6]) |
| Santali | yes / ? | 10 | 48.3 | 49.0 (+0.7 [-1.9, +4.7]) |
| Sindhi | yes / ? | 10 | 60.5 | 61.3 (+0.8 [-2.9, +3.8]) |
| Tamil | yes / ? | 10 | 64.8 | 66.1 (+1.3 [-1.2, +4.3]) |
| Telugu | yes / ? | 10 | 75.8 | 76.7 (+1.0 [-1.8, +5.8]) |
| Urdu | yes / ? | 10 | 75.0 | 75.0 (-0.1 [-3.1, +2.5]) |
| **macro, all (22)** |  | 10 | 67.5 | 68.0 (+0.5 [-0.3, +1.3]) |
| **macro, one script (18)** |  | 10 | 69.7 | 70.1 (+0.4 [-0.5, +1.5]) |

### COMET, mean segment score x 100 (higher is better), English -> X

| language | support | n | indictrans2 | indictrans2-beam5 |
|---|---:|---:|---:|---:|
| Assamese | yes / ? | 10 | 87.3 | 87.4 (+0.1 [-0.6, +0.9]) |
| Bengali | yes / ? | 10 | 89.4 | 89.3 (-0.1 [-0.5, +0.1]) |
| Bodo | yes / ? | 10 | 61.7 | 63.0 (+1.3 [+0.5, +2.1]) |
| Dogri | yes / ? | 10 | 66.4 | 67.4 (+0.9 [-0.1, +2.3]) |
| Konkani | yes / ? | 10 | 60.8 | 61.2 (+0.4 [-0.9, +1.7]) |
| Gujarati | yes / ? | 10 | 91.1 | 91.2 (+0.1 [-0.1, +0.5]) |
| Hindi | yes / ? | 10 | 80.5 | 85.5 (+5.0 [-0.8, +15.4]) |
| Kannada | yes / ? | 10 | 87.8 | 88.0 (+0.2 [-0.8, +1.2]) |
| Kashmiri | yes / ? | 10 | 62.5 | 61.0 (-1.4 [-5.2, +0.8]) |
| Maithili | yes / ? | 10 | 71.0 | 69.4 (-1.6 [-3.9, +0.3]) |
| Malayalam | yes / ? | 10 | 90.2 | 90.2 (-0.1 [-0.7, +0.5]) |
| Marathi | yes / ? | 10 | 80.3 | 81.0 (+0.7 [-0.4, +2.2]) |
| Manipuri | yes / ? | 10 | 84.9 | 86.1 (+1.2 [+0.0, +3.5]) |
| Nepali | yes / ? | 10 | 87.5 | 87.3 (-0.2 [-0.7, +0.3]) |
| Odia | yes / ? | 10 | 79.9 | 79.9 (+0.0 [-0.4, +0.4]) |
| Punjabi | yes / ? | 10 | 86.1 | 86.0 (-0.1 [-0.3, +0.0]) |
| Sanskrit | yes / ? | 10 | 78.7 | 78.7 (+0.1 [-0.4, +0.7]) |
| Santali | yes / ? | 10 | 85.2 | 85.5 (+0.3 [-0.4, +0.9]) |
| Sindhi | yes / ? | 10 | 59.2 | 59.8 (+0.6 [-0.5, +2.2]) |
| Tamil | yes / ? | 10 | 89.1 | 89.2 (+0.1 [-0.6, +0.7]) |
| Telugu | yes / ? | 10 | 88.9 | 88.9 (-0.0 [-0.3, +0.2]) |
| Urdu | yes / ? | 10 | 89.2 | 89.5 (+0.3 [-0.6, +0.9]) |
| **macro, all (22)** |  | 10 | 79.9 | 80.3 (+0.4 [+0.0, +0.9]) |
| **macro, one script (18)** |  | 10 | 81.4 | 81.8 (+0.4 [-0.0, +1.0]) |
| **macro, XLM-R's languages (14)** |  | 10 | 86.1 | 86.6 (+0.4 [-0.1, +1.3]) |

### COMET, mean segment score x 100 (higher is better), X -> English

| language | support | n | indictrans2 | indictrans2-beam5 |
|---|---:|---:|---:|---:|
| Assamese | yes / ? | 10 | 88.1 | 87.7 (-0.5 [-1.4, +0.3]) |
| Bengali | yes / ? | 10 | 89.6 | 89.9 (+0.4 [-0.1, +1.0]) |
| Bodo | yes / ? | 10 | 81.1 | 79.9 (-1.2 [-2.7, +0.0]) |
| Dogri | yes / ? | 10 | 88.9 | 89.3 (+0.4 [+0.0, +0.8]) |
| Konkani | yes / ? | 10 | 84.3 | 84.6 (+0.3 [-0.3, +1.0]) |
| Gujarati | yes / ? | 10 | 91.2 | 91.0 (-0.2 [-0.8, +0.4]) |
| Hindi | yes / ? | 10 | 89.9 | 90.1 (+0.2 [-0.2, +0.6]) |
| Kannada | yes / ? | 10 | 89.1 | 88.3 (-0.8 [-2.4, +0.2]) |
| Kashmiri | yes / ? | 10 | 79.9 | 80.4 (+0.5 [-0.9, +2.6]) |
| Maithili | yes / ? | 10 | 88.4 | 88.7 (+0.3 [+0.1, +0.5]) |
| Malayalam | yes / ? | 10 | 90.6 | 90.9 (+0.3 [-0.1, +0.8]) |
| Marathi | yes / ? | 10 | 89.3 | 89.2 (-0.1 [-0.3, +0.2]) |
| Manipuri | yes / ? | 10 | 78.7 | 78.7 (-0.0 [-1.1, +0.9]) |
| Nepali | yes / ? | 10 | 92.7 | 92.8 (+0.1 [-0.0, +0.4]) |
| Odia | yes / ? | 10 | 90.5 | 90.7 (+0.2 [-0.1, +0.7]) |
| Punjabi | yes / ? | 10 | 89.3 | 89.0 (-0.3 [-0.9, +0.1]) |
| Sanskrit | yes / ? | 10 | 81.3 | 80.4 (-0.9 [-2.7, +0.5]) |
| Santali | yes / ? | 10 | 69.8 | 69.5 (-0.3 [-2.6, +2.1]) |
| Sindhi | yes / ? | 10 | 81.9 | 82.1 (+0.1 [-1.3, +1.5]) |
| Tamil | yes / ? | 10 | 88.9 | 88.9 (-0.0 [-0.7, +0.6]) |
| Telugu | yes / ? | 10 | 91.7 | 91.6 (-0.1 [-0.7, +0.5]) |
| Urdu | yes / ? | 10 | 90.5 | 90.4 (-0.0 [-0.4, +0.2]) |
| **macro, all (22)** |  | 10 | 86.6 | 86.6 (-0.1 [-0.3, +0.1]) |
| **macro, one script (18)** |  | 10 | 88.6 | 88.5 (-0.1 [-0.4, +0.1]) |
| **macro, XLM-R's languages (14)** |  | 10 | 89.5 | 89.4 (-0.1 [-0.4, +0.1]) |

### bits per character of IndicProcessor's pre-processed reference, NOT comparable with the bits above: another text (normalised, tokenised, most Indic scripts transliterated to Devanagari), over the reference's own characters; its end token not counted, English -> X

| language | support | n | indictrans2 |
|---|---:|---:|---:|
| Assamese | yes / ? | 50 | 0.770 |
| Bengali | yes / ? | 50 | 0.575 |
| Bodo | yes / ? | 50 | 0.782 |
| Dogri | yes / ? | 50 | 0.589 |
| Konkani | yes / ? | 50 | 0.905 |
| Gujarati | yes / ? | 50 | 0.610 |
| Hindi | yes / ? | 50 | 0.537 |
| Kannada | yes / ? | 50 | 0.546 |
| Kashmiri | yes / ? | 50 | 1.192 |
| Maithili | yes / ? | 50 | 0.728 |
| Malayalam | yes / ? | 50 | 0.529 |
| Marathi | yes / ? | 50 | 0.515 |
| Manipuri | yes / ? | 50 | 0.981 |
| Nepali | yes / ? | 50 | 0.637 |
| Odia | yes / ? | 50 | 0.595 |
| Punjabi | yes / ? | 50 | 1.005 |
| Sanskrit | yes / ? | 50 | 1.060 |
| Santali | yes / ? | 50 | 1.682 |
| Sindhi | yes / ? | 50 | 1.351 |
| Tamil | yes / ? | 50 | 0.553 |
| Telugu | yes / ? | 50 | 0.620 |
| Urdu | yes / ? | 50 | 0.413 |
| **macro, all (22)** |  | 50 | 0.781 |
| **macro, one script (18)** |  | 50 | 0.665 |

### bits per character of IndicProcessor's pre-processed reference, NOT comparable with the bits above: another text (normalised, tokenised, most Indic scripts transliterated to Devanagari), over the reference's own characters; its end token not counted, X -> English

| language | support | n | indictrans2 |
|---|---:|---:|---:|
| Assamese | yes / ? | 50 | 0.293 |
| Bengali | yes / ? | 50 | 0.292 |
| Bodo | yes / ? | 50 | 0.309 |
| Dogri | yes / ? | 50 | 0.217 |
| Konkani | yes / ? | 50 | 0.364 |
| Gujarati | yes / ? | 50 | 0.292 |
| Hindi | yes / ? | 50 | 0.352 |
| Kannada | yes / ? | 50 | 0.284 |
| Kashmiri | yes / ? | 50 | 0.393 |
| Maithili | yes / ? | 50 | 0.308 |
| Malayalam | yes / ? | 50 | 0.313 |
| Marathi | yes / ? | 50 | 0.294 |
| Manipuri | yes / ? | 50 | 0.346 |
| Nepali | yes / ? | 50 | 0.263 |
| Odia | yes / ? | 50 | 0.260 |
| Punjabi | yes / ? | 50 | 0.415 |
| Sanskrit | yes / ? | 50 | 0.411 |
| Santali | yes / ? | 50 | 0.542 |
| Sindhi | yes / ? | 50 | 0.402 |
| Tamil | yes / ? | 50 | 0.364 |
| Telugu | yes / ? | 50 | 0.322 |
| Urdu | yes / ? | 50 | 0.253 |
| **macro, all (22)** |  | 50 | 0.331 |
| **macro, one script (18)** |  | 50 | 0.311 |

### Tokens per character (the scored references, no BOS; IndicTrans2: of its pre-processed reference, per character of the reference)

| language | characters per sentence | indictrans2 | indictrans2-beam5 |
|---|---:|---:|---:|
| English | 155 | 0.221 | n/a |
| Assamese | 153 | 0.366 | n/a |
| Bengali | 143 | 0.251 | n/a |
| Bodo | 160 | 0.254 | n/a |
| Dogri | 151 | 0.268 | n/a |
| Konkani | 145 | 0.286 | n/a |
| Gujarati | 142 | 0.261 | n/a |
| Hindi | 156 | 0.250 | n/a |
| Kannada | 163 | 0.248 | n/a |
| Kashmiri | 157 | 0.293 | n/a |
| Maithili | 146 | 0.249 | n/a |
| Malayalam | 176 | 0.270 | n/a |
| Marathi | 153 | 0.242 | n/a |
| Manipuri | 149 | 0.334 | n/a |
| Nepali | 148 | 0.236 | n/a |
| Odia | 167 | 0.250 | n/a |
| Punjabi | 140 | 0.338 | n/a |
| Sanskrit | 150 | 0.298 | n/a |
| Santali | 162 | 0.284 | n/a |
| Sindhi | 152 | 0.291 | n/a |
| Tamil | 183 | 0.231 | n/a |
| Telugu | 152 | 0.250 | n/a |
| Urdu | 148 | 0.276 | n/a |

### Speed and memory (generation: greedy)

Not a like-for-like race: engine configs run this repo's sibling engine (Metal INT8/INT4 kernels, continuous batching: a closed loop of `batch` requests in flight); IndicTrans2 runs eager PyTorch through transformers' remote code (static batches of `batch` sources sorted by length, finished rows padded until the batch ends, the encoder run once per batch). Tokens are each model's own (tokens per character below differ), so compare output characters per second. TTFT: from a request's arrival in the engine's queue; for IndicTrans2, from its batch's start (tokenising and the encoder included). One run on one M2 MacBook Air (8 GB), nothing else on the GPU.

| config | stack | weights (GB) | output tok/s | output chars/s | TTFT p50 / p90 (s) | peak GPU (GiB) | peak footprint (GiB) | requests | preempted |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| indictrans2 | hf mps float16 | 2.05 | 115.0 | 514 | 0.35 / 3.98 | 2.26 | 4.32 | 260 | 0 |
| indictrans2-beam5 | hf mps float16 | 2.05 | 26.8 | 114 | 0.08 / 0.43 | 4.22 | 6.39 | 440 | 0 |

### Per-output diagnostics (the directions with any)

none

Scored references whose tokens decode to other text: indictrans2 89 / 2200, indictrans2-beam5 0 / 0 (IndicTrans2: of its pre-processed reference).
Code versions (git describe of this repo and the engine; SHA-256 of eval_translate.py with engine_run.py and the engine's src/, or with indictrans.py) per config: indictrans2 c0df389-dirty b9870acb3fb415a5, c0df389-dirty f6d4f6bc4922a965; indictrans2-beam5 c0df389-dirty b9870acb3fb415a5.
**Warning:** indictrans2's results come from 2 code versions.

### Prompts (each through the model's own chat template; renderings in RUNS/CONFIG/meta.json)

- indictrans2: none: IndicProcessor's language tags (`eng_Latn mni_Mtei TEXT`)
- indictrans2-beam5: none: IndicProcessor's language tags (`eng_Latn mni_Mtei TEXT`)
