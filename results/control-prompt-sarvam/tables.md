chrF++: sacrebleu `nrefs:1|case:mixed|eff:yes|nc:6|nw:2|space:no|version:2.6.0`, corpus level over the sampled ids, on IN22's protocol (IN22-Gen / IndicTrans2 compute_metrics.sh: Indic targets IndicNLP normalize (default options) + trivial_tokenize, English raw; indic-nlp-library 0.92, urduhack 1.1.1). In brackets: the difference from sarvam-int4 and its paired bootstrap 95% CI (1000 resamples, seed 0; a macro row resamples the shared ids jointly over its languages). Support claimed by sarvam-translate. Macro rows: all languages; one script (without Manipuri, Sindhi, Kashmiri, Santali, written in more than one); a config without every language of a row shows -.

COMET: Unbabel/wmt22-comet-da (revision 2760a223, unbabel-comet 2.2.7), reference-based, raw text (no IN22 normalisation), on the CPU. Its encoder (XLM-R) never saw Bodo, Dogri, Konkani, Kashmiri, Maithili, Manipuri, Santali, Sindhi: their COMET is not reliable; the macro over XLM-R's languages leaves them out.

### chrF++ (higher is better), English -> X

| language | support | n | sarvam-int4 | sarvam-int4@neutral |
|---|---:|---:|---:|---:|
| Assamese | yes | 10 | 48.1 | 48.0 (-0.2 [-1.1, +0.4]) |
| Bengali | yes | 10 | 57.1 | 56.7 (-0.4 [-3.3, +2.3]) |
| Bodo | yes | 10 | 44.5 | 44.6 (+0.1 [-0.6, +1.0]) |
| Dogri | yes | 10 | 61.7 | 61.7 (-0.0 [-1.9, +2.4]) |
| Konkani | yes | 10 | 44.1 | 43.4 (-0.7 [-1.6, +0.2]) |
| Gujarati | yes | 10 | 61.3 | 61.8 (+0.4 [+0.0, +1.5]) |
| Hindi | yes | 10 | 60.7 | 59.2 (-1.5 [-4.8, +0.0]) |
| Kannada | yes | 10 | 56.8 | 56.9 (+0.1 [-0.6, +0.9]) |
| Kashmiri | yes | 10 | 39.5 | 40.0 (+0.5 [-1.1, +2.8]) |
| Maithili | yes | 10 | 55.7 | 56.8 (+1.2 [+0.0, +2.5]) |
| Malayalam | yes | 10 | 58.6 | 58.3 (-0.3 [-4.8, +2.6]) |
| Marathi | yes | 10 | 56.4 | 55.4 (-1.0 [-2.7, +1.2]) |
| Manipuri | yes | 10 | 53.6 | 53.6 (-0.0 [-4.1, +2.5]) |
| Nepali | yes | 10 | 56.7 | 55.8 (-1.0 [-3.9, +0.6]) |
| Odia | yes | 10 | 46.6 | 47.6 (+1.1 [+0.0, +2.3]) |
| Punjabi | yes | 10 | 54.3 | 53.8 (-0.5 [-2.8, +0.7]) |
| Sanskrit | yes | 10 | 43.9 | 43.4 (-0.5 [-1.3, -0.0]) |
| Santali | yes | 10 | 42.6 | 43.6 (+1.0 [-0.2, +1.8]) |
| Sindhi | yes | 10 | 40.3 | 40.2 (-0.1 [-0.6, +0.3]) |
| Tamil | yes | 10 | 48.4 | 48.7 (+0.3 [-1.1, +1.4]) |
| Telugu | yes | 10 | 62.7 | 62.1 (-0.6 [-1.5, +0.0]) |
| Urdu | yes | 10 | 73.4 | 73.6 (+0.2 [-0.7, +0.9]) |
| **macro, all (22)** |  | 10 | 53.1 | 53.0 (-0.1 [-0.7, +0.3]) |
| **macro, one script (18)** |  | 10 | 55.1 | 54.9 (-0.2 [-0.7, +0.1]) |

### chrF++ (higher is better), X -> English

| language | support | n | sarvam-int4 | sarvam-int4@neutral |
|---|---:|---:|---:|---:|
| Assamese | yes | 10 | 30.0 | 56.8 (+26.8 [-6.5, +42.3]) |
| Bengali | yes | 10 | 57.8 | 58.3 (+0.4 [-4.6, +5.0]) |
| Bodo | yes | 10 | 50.5 | 46.4 (-4.1 [-16.2, +2.8]) |
| Dogri | yes | 10 | 56.9 | 52.6 (-4.3 [-15.8, +2.0]) |
| Konkani | yes | 10 | 54.0 | 45.3 (-8.7 [-19.5, +0.7]) |
| Gujarati | yes | 10 | 58.4 | 62.3 (+3.9 [-3.8, +11.9]) |
| Hindi | yes | 10 | 58.2 | 68.1 (+9.9 [+4.9, +14.2]) |
| Kannada | yes | 10 | 57.2 | 62.6 (+5.4 [+1.0, +10.8]) |
| Kashmiri | yes | 10 | 47.7 | 45.5 (-2.2 [-14.1, +6.2]) |
| Maithili | yes | 10 | 61.2 | 64.0 (+2.8 [-2.6, +9.9]) |
| Malayalam | yes | 10 | 59.4 | 59.0 (-0.4 [-3.2, +2.4]) |
| Marathi | yes | 10 | 54.6 | 59.4 (+4.8 [-1.6, +10.1]) |
| Manipuri | yes | 10 | 53.0 | 25.8 (-27.2 [-44.8, -10.5]) |
| Nepali | yes | 10 | 58.5 | 60.6 (+2.0 [-6.7, +10.9]) |
| Odia | yes | 10 | 54.7 | 54.9 (+0.2 [-2.3, +2.4]) |
| Punjabi | yes | 10 | 51.7 | 60.0 (+8.4 [+3.4, +11.6]) |
| Sanskrit | yes | 10 | 50.1 | 53.0 (+3.0 [-1.5, +6.5]) |
| Santali | yes | 10 | 44.8 | 32.1 (-12.7 [-24.4, -2.5]) |
| Sindhi | yes | 10 | 49.6 | 47.4 (-2.2 [-20.0, +10.6]) |
| Tamil | yes | 10 | 53.9 | 57.7 (+3.8 [+0.0, +6.4]) |
| Telugu | yes | 10 | 59.4 | 59.7 (+0.3 [-3.3, +4.2]) |
| Urdu | yes | 10 | 62.1 | 61.8 (-0.3 [-4.8, +4.0]) |
| **macro, all (22)** |  | 10 | 53.8 | 54.2 (+0.4 [-3.8, +3.6]) |
| **macro, one script (18)** |  | 10 | 54.9 | 57.9 (+3.0 [-1.0, +5.5]) |

### COMET, mean segment score x 100 (higher is better), English -> X

| language | support | n | sarvam-int4 | sarvam-int4@neutral |
|---|---:|---:|---:|---:|
| Assamese | yes | 10 | 88.6 | 88.1 (-0.4 [-1.4, +0.1]) |
| Bengali | yes | 10 | 90.2 | 90.0 (-0.2 [-0.4, +0.0]) |
| Bodo | yes | 10 | 61.0 | 61.2 (+0.2 [-0.5, +1.0]) |
| Dogri | yes | 10 | 66.7 | 67.8 (+1.1 [-1.1, +4.0]) |
| Konkani | yes | 10 | 60.2 | 60.0 (-0.1 [-1.2, +0.9]) |
| Gujarati | yes | 10 | 91.9 | 91.8 (-0.1 [-0.7, +0.2]) |
| Hindi | yes | 10 | 85.3 | 85.0 (-0.3 [-0.8, +0.0]) |
| Kannada | yes | 10 | 87.9 | 87.8 (-0.0 [-0.4, +0.2]) |
| Kashmiri | yes | 10 | 68.8 | 67.1 (-1.7 [-4.8, +1.2]) |
| Maithili | yes | 10 | 70.9 | 71.5 (+0.6 [+0.1, +1.2]) |
| Malayalam | yes | 10 | 90.3 | 90.0 (-0.2 [-1.0, +0.4]) |
| Marathi | yes | 10 | 81.4 | 80.9 (-0.5 [-0.9, -0.0]) |
| Manipuri | yes | 10 | 87.9 | 88.3 (+0.4 [-0.2, +1.0]) |
| Nepali | yes | 10 | 86.8 | 86.8 (+0.1 [-0.2, +0.4]) |
| Odia | yes | 10 | 87.1 | 87.4 (+0.3 [-0.1, +0.8]) |
| Punjabi | yes | 10 | 86.0 | 85.9 (-0.1 [-0.5, +0.3]) |
| Sanskrit | yes | 10 | 82.7 | 82.8 (+0.1 [-0.2, +0.3]) |
| Santali | yes | 10 | 89.8 | 89.5 (-0.4 [-1.1, +0.2]) |
| Sindhi | yes | 10 | 61.2 | 61.2 (-0.0 [-0.7, +0.7]) |
| Tamil | yes | 10 | 90.8 | 90.6 (-0.2 [-0.6, +0.0]) |
| Telugu | yes | 10 | 89.9 | 89.5 (-0.4 [-1.5, +0.4]) |
| Urdu | yes | 10 | 90.2 | 90.0 (-0.2 [-0.4, -0.0]) |
| **macro, all (22)** |  | 10 | 81.6 | 81.5 (-0.1 [-0.3, +0.1]) |
| **macro, one script (18)** |  | 10 | 82.6 | 82.6 (-0.0 [-0.2, +0.2]) |
| **macro, XLM-R's languages (14)** |  | 10 | 87.8 | 87.6 (-0.2 [-0.3, -0.0]) |

### COMET, mean segment score x 100 (higher is better), X -> English

| language | support | n | sarvam-int4 | sarvam-int4@neutral |
|---|---:|---:|---:|---:|
| Assamese | yes | 10 | 83.7 | 86.0 (+2.3 [-1.7, +9.4]) |
| Bengali | yes | 10 | 88.3 | 88.2 (-0.1 [-2.3, +1.6]) |
| Bodo | yes | 10 | 75.0 | 72.4 (-2.6 [-14.3, +5.8]) |
| Dogri | yes | 10 | 83.6 | 81.0 (-2.6 [-12.3, +3.4]) |
| Konkani | yes | 10 | 82.3 | 75.0 (-7.3 [-19.5, +0.7]) |
| Gujarati | yes | 10 | 88.6 | 87.8 (-0.8 [-3.3, +1.4]) |
| Hindi | yes | 10 | 89.2 | 90.8 (+1.6 [+0.8, +2.4]) |
| Kannada | yes | 10 | 87.0 | 87.8 (+0.7 [+0.1, +1.5]) |
| Kashmiri | yes | 10 | 79.6 | 72.5 (-7.1 [-16.3, +0.7]) |
| Maithili | yes | 10 | 84.6 | 85.7 (+1.1 [-1.0, +4.3]) |
| Malayalam | yes | 10 | 88.0 | 87.7 (-0.4 [-1.2, +0.6]) |
| Marathi | yes | 10 | 86.2 | 86.8 (+0.7 [-2.0, +2.7]) |
| Manipuri | yes | 10 | 76.0 | 40.1 (-36.0 [-54.5, -16.9]) |
| Nepali | yes | 10 | 90.0 | 91.0 (+1.0 [-0.6, +2.6]) |
| Odia | yes | 10 | 87.7 | 89.1 (+1.4 [-0.1, +2.9]) |
| Punjabi | yes | 10 | 86.6 | 89.0 (+2.5 [+0.9, +4.2]) |
| Sanskrit | yes | 10 | 84.4 | 84.7 (+0.3 [-1.4, +1.9]) |
| Santali | yes | 10 | 70.5 | 59.5 (-11.0 [-24.0, -1.2]) |
| Sindhi | yes | 10 | 81.9 | 77.6 (-4.4 [-17.3, +3.4]) |
| Tamil | yes | 10 | 85.2 | 87.2 (+1.9 [-1.2, +6.0]) |
| Telugu | yes | 10 | 88.1 | 88.3 (+0.2 [-0.6, +1.2]) |
| Urdu | yes | 10 | 88.5 | 87.3 (-1.1 [-2.7, +0.1]) |
| **macro, all (22)** |  | 10 | 84.3 | 81.6 (-2.7 [-5.3, -0.6]) |
| **macro, one script (18)** |  | 10 | 85.9 | 85.9 (-0.1 [-1.7, +1.1]) |
| **macro, XLM-R's languages (14)** |  | 10 | 87.3 | 88.0 (+0.7 [+0.1, +1.6]) |

### bits per reference character (lower is better), English -> X

| language | support | n | sarvam-int4 |
|---|---:|---:|---:|
| Assamese | yes | 50 | 0.619 |
| Bengali | yes | 50 | 0.501 |
| Bodo | yes | 50 | 0.631 |
| Dogri | yes | 50 | 0.453 |
| Konkani | yes | 50 | 0.725 |
| Gujarati | yes | 50 | 0.541 |
| Hindi | yes | 50 | 0.448 |
| Kannada | yes | 50 | 0.468 |
| Kashmiri | yes | 50 | 1.026 |
| Maithili | yes | 50 | 0.648 |
| Malayalam | yes | 50 | 0.461 |
| Marathi | yes | 50 | 0.441 |
| Manipuri | yes | 50 | 0.744 |
| Nepali | yes | 50 | 0.542 |
| Odia | yes | 50 | 0.517 |
| Punjabi | yes | 50 | 0.938 |
| Sanskrit | yes | 50 | 0.835 |
| Santali | yes | 50 | 1.081 |
| Sindhi | yes | 50 | 1.032 |
| Tamil | yes | 50 | 0.444 |
| Telugu | yes | 50 | 0.540 |
| Urdu | yes | 50 | 0.358 |
| **macro, all (22)** |  | 50 | 0.636 |
| **macro, one script (18)** |  | 50 | 0.561 |

### bits per reference character (lower is better), X -> English

| language | support | n | sarvam-int4 |
|---|---:|---:|---:|
| Assamese | yes | 50 | 0.497 |
| Bengali | yes | 50 | 0.502 |
| Bodo | yes | 50 | 0.555 |
| Dogri | yes | 50 | 0.456 |
| Konkani | yes | 50 | 0.605 |
| Gujarati | yes | 50 | 0.502 |
| Hindi | yes | 50 | 0.528 |
| Kannada | yes | 50 | 0.490 |
| Kashmiri | yes | 50 | 0.587 |
| Maithili | yes | 50 | 0.501 |
| Malayalam | yes | 50 | 0.507 |
| Marathi | yes | 50 | 0.509 |
| Manipuri | yes | 50 | 0.541 |
| Nepali | yes | 50 | 0.464 |
| Odia | yes | 50 | 0.471 |
| Punjabi | yes | 50 | 0.588 |
| Sanskrit | yes | 50 | 0.605 |
| Santali | yes | 50 | 0.611 |
| Sindhi | yes | 50 | 0.571 |
| Tamil | yes | 50 | 0.551 |
| Telugu | yes | 50 | 0.529 |
| Urdu | yes | 50 | 0.464 |
| **macro, all (22)** |  | 50 | 0.529 |
| **macro, one script (18)** |  | 50 | 0.518 |

### bits per reference character with the end-of-answer token (lower is better), English -> X

| language | support | n | sarvam-int4 |
|---|---:|---:|---:|
| Assamese | yes | 50 | 0.619 |
| Bengali | yes | 50 | 0.501 |
| Bodo | yes | 50 | 0.631 |
| Dogri | yes | 50 | 0.453 |
| Konkani | yes | 50 | 0.725 |
| Gujarati | yes | 50 | 0.542 |
| Hindi | yes | 50 | 0.448 |
| Kannada | yes | 50 | 0.468 |
| Kashmiri | yes | 50 | 1.026 |
| Maithili | yes | 50 | 0.648 |
| Malayalam | yes | 50 | 0.461 |
| Marathi | yes | 50 | 0.441 |
| Manipuri | yes | 50 | 0.744 |
| Nepali | yes | 50 | 0.542 |
| Odia | yes | 50 | 0.517 |
| Punjabi | yes | 50 | 0.938 |
| Sanskrit | yes | 50 | 0.835 |
| Santali | yes | 50 | 1.081 |
| Sindhi | yes | 50 | 1.032 |
| Tamil | yes | 50 | 0.444 |
| Telugu | yes | 50 | 0.540 |
| Urdu | yes | 50 | 0.360 |
| **macro, all (22)** |  | 50 | 0.636 |
| **macro, one script (18)** |  | 50 | 0.562 |

### bits per reference character with the end-of-answer token (lower is better), X -> English

| language | support | n | sarvam-int4 |
|---|---:|---:|---:|
| Assamese | yes | 50 | 0.497 |
| Bengali | yes | 50 | 0.502 |
| Bodo | yes | 50 | 0.555 |
| Dogri | yes | 50 | 0.456 |
| Konkani | yes | 50 | 0.605 |
| Gujarati | yes | 50 | 0.502 |
| Hindi | yes | 50 | 0.528 |
| Kannada | yes | 50 | 0.490 |
| Kashmiri | yes | 50 | 0.587 |
| Maithili | yes | 50 | 0.501 |
| Malayalam | yes | 50 | 0.507 |
| Marathi | yes | 50 | 0.509 |
| Manipuri | yes | 50 | 0.541 |
| Nepali | yes | 50 | 0.464 |
| Odia | yes | 50 | 0.471 |
| Punjabi | yes | 50 | 0.588 |
| Sanskrit | yes | 50 | 0.605 |
| Santali | yes | 50 | 0.611 |
| Sindhi | yes | 50 | 0.571 |
| Tamil | yes | 50 | 0.551 |
| Telugu | yes | 50 | 0.529 |
| Urdu | yes | 50 | 0.464 |
| **macro, all (22)** |  | 50 | 0.529 |
| **macro, one script (18)** |  | 50 | 0.518 |

### Tokens per character (the scored references, no BOS; IndicTrans2: of its pre-processed reference, per character of the reference)

| language | characters per sentence | sarvam-translate |
|---|---:|---:|
| English | 155 | 0.214 |
| Assamese | 153 | 0.411 |
| Bengali | 143 | 0.280 |
| Bodo | 160 | 0.457 |
| Dogri | 151 | 0.374 |
| Konkani | 145 | 0.410 |
| Gujarati | 142 | 0.433 |
| Hindi | 156 | 0.281 |
| Kannada | 163 | 0.408 |
| Kashmiri | 157 | 0.570 |
| Maithili | 146 | 0.347 |
| Malayalam | 176 | 0.363 |
| Marathi | 153 | 0.302 |
| Manipuri | 149 | 1.830 |
| Nepali | 148 | 0.325 |
| Odia | 167 | 0.730 |
| Punjabi | 140 | 0.569 |
| Sanskrit | 150 | 0.408 |
| Santali | 162 | 1.016 |
| Sindhi | 152 | 0.432 |
| Tamil | 183 | 0.282 |
| Telugu | 152 | 0.390 |
| Urdu | 148 | 0.335 |

### Speed and memory (generation: greedy)

Not a like-for-like race: engine configs run this repo's sibling engine (Metal INT8/INT4 kernels, continuous batching: a closed loop of `batch` requests in flight); IndicTrans2 runs eager PyTorch through transformers' remote code (static batches of `batch` sources sorted by length, finished rows padded until the batch ends, the encoder run once per batch). Tokens are each model's own (tokens per character below differ), so compare output characters per second. TTFT: from a request's arrival in the engine's queue; for IndicTrans2, from its batch's start (tokenising and the encoder included). One run on one M2 MacBook Air (8 GB), nothing else on the GPU.

| config | stack | weights (GB) | output tok/s | output chars/s | TTFT p50 / p90 (s) | peak GPU (GiB) | peak footprint (GiB) | requests | preempted |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sarvam-int4 | metal-int4 | 2.99 | 21.0 | 59 | 1.02 / 1.83 | 4.52 | 5.57 | 2136 | 1 |
| sarvam-int4@neutral | metal-int4 | 2.99 | 26.8 | 71 | 0.90 / 1.67 | 3.74 | 4.81 | 440 | 0 |

### Per-output diagnostics (the directions with any)

| config | direction | outputs | under 50% in the target's script (letters) | stopped by max_new_tokens | with special tokens (removed before scoring) | with other added tokens (kept) |
|---|---:|---:|---:|---:|---:|---:|
| sarvam-int4 | asm-eng | 50 | 0 | 1 | 0 | 0 |
| sarvam-int4 | eng-brx | 50 | 0 | 1 | 0 | 0 |
| sarvam-int4 | eng-npi | 50 | 0 | 1 | 0 | 0 |
| sarvam-int4 | eng-sat | 50 | 0 | 2 | 0 | 0 |
| sarvam-int4 | eng-snd | 50 | 1 | 1 | 0 | 0 |
| sarvam-int4 | kas-eng | 50 | 0 | 1 | 0 | 0 |
| sarvam-int4@neutral | brx-eng | 10 | 1 | 0 | 0 | 0 |
| sarvam-int4@neutral | doi-eng | 10 | 1 | 0 | 0 | 0 |
| sarvam-int4@neutral | eng-brx | 10 | 0 | 1 | 0 | 0 |
| sarvam-int4@neutral | gom-eng | 10 | 1 | 0 | 0 | 0 |
| sarvam-int4@neutral | kas-eng | 10 | 1 | 0 | 0 | 0 |
| sarvam-int4@neutral | mni-eng | 10 | 6 | 0 | 0 | 0 |
| sarvam-int4@neutral | sat-eng | 10 | 2 | 0 | 0 | 0 |
| sarvam-int4@neutral | snd-eng | 10 | 1 | 0 | 0 | 0 |

Scored references whose tokens decode to other text: sarvam-int4 0 / 2200, sarvam-int4@neutral 0 / 0 (IndicTrans2: of its pre-processed reference).
Code versions (git describe of this repo and the engine; SHA-256 of eval_translate.py with engine_run.py and the engine's src/, or with indictrans.py) per config: sarvam-int4 6f1a79b-dirty 445a9d6ffbd7446e, 9eaa6eb-dirty 2c76e3989512f1e0, a9cbe98-dirty 28b60036a2537030; sarvam-int4@neutral c0df389-dirty engine 324313a-dirty 626af229de5f2f07.
**Warning:** sarvam-int4's results come from 3 code versions.

### Prompts (each through the model's own chat template; renderings in RUNS/CONFIG/meta.json)

- sarvam-int4: `[{"role": "system", "content": "Translate the text below to {Target}."}, {"role": "user", "content": "{text}"}]`
- sarvam-int4@neutral: `[{"role": "user", "content": "Translate the following text from {Source} to {Target}. Reply with the translation only.\n\n{text}"}]`
