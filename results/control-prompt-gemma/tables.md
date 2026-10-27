chrF++: sacrebleu `nrefs:1|case:mixed|eff:yes|nc:6|nw:2|space:no|version:2.6.0`, corpus level over the sampled ids, on IN22's protocol (IN22-Gen / IndicTrans2 compute_metrics.sh: Indic targets IndicNLP normalize (default options) + trivial_tokenize, English raw; indic-nlp-library 0.92, urduhack 1.1.1). In brackets: the difference from gemma-int4@neutral and its paired bootstrap 95% CI (1000 resamples, seed 0; a macro row resamples the shared ids jointly over its languages). Support claimed by gemma-3-4b-it. Macro rows: all languages; one script (without Manipuri, Sindhi, Kashmiri, Santali, written in more than one); a config without every language of a row shows -.

COMET: Unbabel/wmt22-comet-da (revision 2760a223, unbabel-comet 2.2.7), reference-based, raw text (no IN22 normalisation), on the CPU. Its encoder (XLM-R) never saw Bodo, Dogri, Konkani, Kashmiri, Maithili, Manipuri, Santali, Sindhi: their COMET is not reliable; the macro over XLM-R's languages leaves them out.

### chrF++ (higher is better), English -> X

| language | support | n | gemma-int4@neutral | gemma-int4 |
|---|---:|---:|---:|---:|
| Assamese | ? | 3 | 23.6 | 12.6 (-11.0 [-12.2, -6.2]) |
| Bengali | ? | 3 | 43.1 | 17.0 (-26.1 [-42.9, -8.1]) |
| Bodo | ? | 3 | 1.3 | 3.8 (+2.6 [-1.7, +5.0]) |
| Dogri | ? | 3 | 23.5 | 3.5 (-20.1 [-30.1, -1.5]) |
| Konkani | ? | 3 | 2.1 | 3.5 (+1.5 [-0.9, +5.3]) |
| Gujarati | ? | 3 | 42.5 | 18.7 (-23.9 [-32.7, -17.0]) |
| Hindi | ? | 3 | 63.5 | 24.9 (-38.6 [-55.2, -26.6]) |
| Kannada | ? | 3 | 24.4 | 12.5 (-11.9 [-34.8, -1.6]) |
| Kashmiri | ? | 3 | 6.6 | 3.8 (-2.8 [-9.8, +1.6]) |
| Maithili | ? | 3 | 32.1 | 12.1 (-19.9 [-22.1, -14.8]) |
| Malayalam | ? | 3 | 17.7 | 7.3 (-10.4 [-21.5, -2.9]) |
| Marathi | ? | 3 | 50.9 | 20.1 (-30.8 [-40.1, -21.9]) |
| Manipuri | ? | 3 | 1.4 | 0.5 (-0.9 [-3.2, +0.6]) |
| Nepali | ? | 3 | 43.4 | 16.7 (-26.7 [-31.0, -21.8]) |
| Odia | ? | 3 | 6.3 | 12.5 (+6.2 [-1.8, +12.7]) |
| Punjabi | ? | 3 | 32.6 | 15.8 (-16.9 [-17.2, -12.6]) |
| Sanskrit | ? | 3 | 19.3 | 8.6 (-10.7 [-15.8, -8.7]) |
| Santali | ? | 3 | 1.4 | 0.5 (-0.9 [-1.0, -0.4]) |
| Sindhi | ? | 3 | 1.0 | 0.9 (-0.1 [-1.6, +0.3]) |
| Tamil | ? | 3 | 47.2 | 20.9 (-26.3 [-36.4, -20.9]) |
| Telugu | ? | 3 | 54.9 | 21.9 (-33.0 [-35.4, -27.6]) |
| Urdu | ? | 3 | 53.3 | 20.3 (-33.0 [-49.9, -23.6]) |
| **macro, all (22)** |  | 3 | 26.9 | 11.7 (-15.2 [-18.0, -11.7]) |
| **macro, one script (18)** |  | 3 | 32.3 | 14.0 (-18.3 [-21.7, -13.8]) |

### chrF++ (higher is better), X -> English

| language | support | n | gemma-int4@neutral | gemma-int4 |
|---|---:|---:|---:|---:|
| Assamese | ? | 3 | 58.0 | 43.0 (-14.9 [-17.9, -12.3]) |
| Bengali | ? | 3 | 54.1 | 51.3 (-2.8 [-23.5, +14.0]) |
| Bodo | ? | 3 | 24.2 | 15.0 (-9.1 [-14.0, -7.8]) |
| Dogri | ? | 3 | 47.7 | 39.8 (-7.8 [-8.2, -1.0]) |
| Konkani | ? | 3 | 49.5 | 36.9 (-12.6 [-18.2, -6.3]) |
| Gujarati | ? | 3 | 63.3 | 53.0 (-10.3 [-11.7, -4.0]) |
| Hindi | ? | 3 | 62.5 | 48.7 (-13.8 [-22.9, -0.3]) |
| Kannada | ? | 3 | 58.0 | 50.8 (-7.1 [-23.2, +8.5]) |
| Kashmiri | ? | 3 | 41.3 | 36.6 (-4.6 [-9.5, +2.8]) |
| Maithili | ? | 3 | 63.1 | 40.0 (-23.1 [-24.2, -15.0]) |
| Malayalam | ? | 3 | 60.2 | 47.9 (-12.3 [-23.2, +1.3]) |
| Marathi | ? | 3 | 67.2 | 50.2 (-17.0 [-25.8, -0.4]) |
| Manipuri | ? | 3 | 21.4 | 16.5 (-4.9 [-9.9, -2.1]) |
| Nepali | ? | 3 | 59.4 | 48.0 (-11.4 [-21.2, -2.7]) |
| Odia | ? | 3 | 56.1 | 46.3 (-9.8 [-24.0, -5.7]) |
| Punjabi | ? | 3 | 56.3 | 53.4 (-2.9 [-10.4, +8.0]) |
| Sanskrit | ? | 3 | 49.4 | 29.5 (-19.9 [-33.4, -3.0]) |
| Santali | ? | 3 | 28.4 | 28.4 (+0.1 [-4.0, +3.9]) |
| Sindhi | ? | 3 | 29.9 | 19.6 (-10.3 [-17.1, -4.6]) |
| Tamil | ? | 3 | 53.9 | 40.4 (-13.5 [-40.1, +0.6]) |
| Telugu | ? | 3 | 72.5 | 59.2 (-13.4 [-19.0, -3.5]) |
| Urdu | ? | 3 | 64.1 | 47.8 (-16.4 [-30.0, -2.4]) |
| **macro, all (22)** |  | 3 | 51.8 | 41.0 (-10.8 [-15.0, -4.5]) |
| **macro, one script (18)** |  | 3 | 56.6 | 44.5 (-12.1 [-16.8, -4.8]) |

### COMET, mean segment score x 100 (higher is better), English -> X

| language | support | n | gemma-int4@neutral | gemma-int4 |
|---|---:|---:|---:|---:|
| Assamese | ? | 3 | 72.2 | 39.4 (-32.8 [-39.5, -26.4]) |
| Bengali | ? | 3 | 89.0 | 46.3 (-42.7 [-52.5, -24.5]) |
| Bodo | ? | 3 | 26.1 | 27.2 (+1.1 [-6.4, +6.0]) |
| Dogri | ? | 3 | 51.5 | 32.3 (-19.2 [-29.6, -13.3]) |
| Konkani | ? | 3 | 42.7 | 30.1 (-12.6 [-28.1, +3.2]) |
| Gujarati | ? | 3 | 89.5 | 44.0 (-45.5 [-52.6, -37.4]) |
| Hindi | ? | 3 | 84.4 | 43.0 (-41.3 [-47.7, -36.0]) |
| Kannada | ? | 3 | 77.5 | 38.7 (-38.7 [-47.6, -25.0]) |
| Kashmiri | ? | 3 | 34.6 | 35.6 (+1.0 [-1.2, +4.4]) |
| Maithili | ? | 3 | 66.1 | 34.0 (-32.1 [-42.7, -19.3]) |
| Malayalam | ? | 3 | 66.5 | 35.9 (-30.6 [-47.4, -22.1]) |
| Marathi | ? | 3 | 79.0 | 32.7 (-46.3 [-52.4, -37.8]) |
| Manipuri | ? | 3 | 77.0 | 53.1 (-23.9 [-48.9, -2.5]) |
| Nepali | ? | 3 | 83.4 | 33.1 (-50.3 [-55.2, -44.4]) |
| Odia | ? | 3 | 50.5 | 33.3 (-17.1 [-45.5, +8.9]) |
| Punjabi | ? | 3 | 73.0 | 41.9 (-31.1 [-41.6, -17.7]) |
| Sanskrit | ? | 3 | 60.3 | 28.6 (-31.7 [-39.9, -25.2]) |
| Santali | ? | 3 | 16.1 | 17.6 (+1.4 [-1.9, +3.4]) |
| Sindhi | ? | 3 | 32.0 | 30.2 (-1.8 [-12.5, +17.2]) |
| Tamil | ? | 3 | 91.5 | 43.5 (-48.1 [-53.8, -44.6]) |
| Telugu | ? | 3 | 88.5 | 45.6 (-42.9 [-47.6, -35.0]) |
| Urdu | ? | 3 | 83.9 | 41.2 (-42.7 [-53.2, -35.6]) |
| **macro, all (22)** |  | 3 | 65.2 | 36.7 (-28.5 [-32.6, -22.4]) |
| **macro, one script (18)** |  | 3 | 70.9 | 37.3 (-33.6 [-37.0, -28.1]) |
| **macro, XLM-R's languages (14)** |  | 3 | 77.8 | 39.1 (-38.7 [-43.4, -31.0]) |

### COMET, mean segment score x 100 (higher is better), X -> English

| language | support | n | gemma-int4@neutral | gemma-int4 |
|---|---:|---:|---:|---:|
| Assamese | ? | 3 | 86.6 | 70.5 (-16.1 [-29.6, -3.3]) |
| Bengali | ? | 3 | 87.8 | 72.8 (-15.0 [-36.1, +0.7]) |
| Bodo | ? | 3 | 53.8 | 47.0 (-6.8 [-17.5, +8.3]) |
| Dogri | ? | 3 | 82.0 | 52.8 (-29.2 [-38.1, -24.3]) |
| Konkani | ? | 3 | 80.5 | 64.1 (-16.4 [-21.5, -12.7]) |
| Gujarati | ? | 3 | 89.5 | 79.8 (-9.6 [-21.4, -0.5]) |
| Hindi | ? | 3 | 90.4 | 76.8 (-13.6 [-19.5, -2.5]) |
| Kannada | ? | 3 | 88.5 | 67.7 (-20.7 [-41.9, -0.7]) |
| Kashmiri | ? | 3 | 76.0 | 60.5 (-15.5 [-17.3, -13.8]) |
| Maithili | ? | 3 | 84.3 | 62.1 (-22.2 [-23.3, -21.4]) |
| Malayalam | ? | 3 | 89.7 | 75.5 (-14.2 [-29.6, -3.1]) |
| Marathi | ? | 3 | 89.7 | 80.1 (-9.6 [-23.5, -1.3]) |
| Manipuri | ? | 3 | 43.9 | 43.4 (-0.5 [-2.0, +0.6]) |
| Nepali | ? | 3 | 91.3 | 82.7 (-8.6 [-17.1, -4.1]) |
| Odia | ? | 3 | 87.2 | 71.7 (-15.5 [-27.5, -3.0]) |
| Punjabi | ? | 3 | 83.4 | 79.5 (-3.9 [-11.7, +0.5]) |
| Sanskrit | ? | 3 | 82.5 | 59.9 (-22.6 [-29.8, -9.6]) |
| Santali | ? | 3 | 60.4 | 53.2 (-7.2 [-12.7, -1.4]) |
| Sindhi | ? | 3 | 67.9 | 48.5 (-19.4 [-20.9, -16.6]) |
| Tamil | ? | 3 | 87.3 | 74.0 (-13.2 [-26.3, -1.0]) |
| Telugu | ? | 3 | 90.0 | 80.9 (-9.1 [-15.9, -3.6]) |
| Urdu | ? | 3 | 89.2 | 76.9 (-12.4 [-28.6, +1.1]) |
| **macro, all (22)** |  | 3 | 81.0 | 67.3 (-13.7 [-18.9, -6.3]) |
| **macro, one script (18)** |  | 3 | 85.2 | 70.8 (-14.4 [-20.5, -5.7]) |
| **macro, XLM-R's languages (14)** |  | 3 | 88.1 | 74.9 (-13.2 [-21.2, -2.2]) |

### bits per reference character (lower is better), English -> X

| language | support | n | gemma-int4@neutral |
|---|---:|---:|---:|
| Assamese | ? | 50 | 3.123 |
| Bengali | ? | 50 | 1.584 |
| Bodo | ? | 50 | 4.149 |
| Dogri | ? | 50 | 3.018 |
| Konkani | ? | 50 | 3.930 |
| Gujarati | ? | 50 | 1.777 |
| Hindi | ? | 50 | 1.181 |
| Kannada | ? | 50 | 2.340 |
| Kashmiri | ? | 50 | 4.891 |
| Maithili | ? | 50 | 2.724 |
| Malayalam | ? | 50 | 2.186 |
| Marathi | ? | 50 | 1.469 |
| Manipuri | ? | 50 | 5.850 |
| Nepali | ? | 50 | 2.102 |
| Odia | ? | 50 | 3.537 |
| Punjabi | ? | 50 | 3.033 |
| Sanskrit | ? | 50 | 3.387 |
| Santali | ? | 50 | 4.887 |
| Sindhi | ? | 50 | 4.718 |
| Tamil | ? | 50 | 1.188 |
| Telugu | ? | 50 | 1.668 |
| Urdu | ? | 50 | 1.421 |
| **macro, all (22)** |  | 50 | 2.917 |
| **macro, one script (18)** |  | 50 | 2.434 |

### bits per reference character (lower is better), X -> English

| language | support | n | gemma-int4@neutral |
|---|---:|---:|---:|
| Assamese | ? | 50 | 1.387 |
| Bengali | ? | 50 | 1.100 |
| Bodo | ? | 50 | 1.601 |
| Dogri | ? | 50 | 1.313 |
| Konkani | ? | 50 | 1.528 |
| Gujarati | ? | 50 | 1.087 |
| Hindi | ? | 50 | 1.188 |
| Kannada | ? | 50 | 1.188 |
| Kashmiri | ? | 50 | 1.557 |
| Maithili | ? | 50 | 1.292 |
| Malayalam | ? | 50 | 1.317 |
| Marathi | ? | 50 | 1.190 |
| Manipuri | ? | 50 | 1.872 |
| Nepali | ? | 50 | 1.104 |
| Odia | ? | 50 | 1.324 |
| Punjabi | ? | 50 | 1.374 |
| Sanskrit | ? | 50 | 1.611 |
| Santali | ? | 50 | 1.590 |
| Sindhi | ? | 50 | 1.461 |
| Tamil | ? | 50 | 1.311 |
| Telugu | ? | 50 | 1.168 |
| Urdu | ? | 50 | 0.974 |
| **macro, all (22)** |  | 50 | 1.343 |
| **macro, one script (18)** |  | 50 | 1.281 |

### bits per reference character with the end-of-answer token (lower is better), English -> X

| language | support | n | gemma-int4@neutral |
|---|---:|---:|---:|
| Assamese | ? | 50 | 3.123 |
| Bengali | ? | 50 | 1.584 |
| Bodo | ? | 50 | 4.149 |
| Dogri | ? | 50 | 3.018 |
| Konkani | ? | 50 | 3.933 |
| Gujarati | ? | 50 | 1.780 |
| Hindi | ? | 50 | 1.181 |
| Kannada | ? | 50 | 2.347 |
| Kashmiri | ? | 50 | 4.893 |
| Maithili | ? | 50 | 2.724 |
| Malayalam | ? | 50 | 2.188 |
| Marathi | ? | 50 | 1.469 |
| Manipuri | ? | 50 | 5.860 |
| Nepali | ? | 50 | 2.102 |
| Odia | ? | 50 | 3.539 |
| Punjabi | ? | 50 | 3.035 |
| Sanskrit | ? | 50 | 3.390 |
| Santali | ? | 50 | 4.889 |
| Sindhi | ? | 50 | 4.720 |
| Tamil | ? | 50 | 1.188 |
| Telugu | ? | 50 | 1.668 |
| Urdu | ? | 50 | 1.421 |
| **macro, all (22)** |  | 50 | 2.918 |
| **macro, one script (18)** |  | 50 | 2.436 |

### bits per reference character with the end-of-answer token (lower is better), X -> English

| language | support | n | gemma-int4@neutral |
|---|---:|---:|---:|
| Assamese | ? | 50 | 1.387 |
| Bengali | ? | 50 | 1.100 |
| Bodo | ? | 50 | 1.607 |
| Dogri | ? | 50 | 1.317 |
| Konkani | ? | 50 | 1.531 |
| Gujarati | ? | 50 | 1.087 |
| Hindi | ? | 50 | 1.188 |
| Kannada | ? | 50 | 1.188 |
| Kashmiri | ? | 50 | 1.562 |
| Maithili | ? | 50 | 1.292 |
| Malayalam | ? | 50 | 1.317 |
| Marathi | ? | 50 | 1.190 |
| Manipuri | ? | 50 | 1.912 |
| Nepali | ? | 50 | 1.104 |
| Odia | ? | 50 | 1.324 |
| Punjabi | ? | 50 | 1.374 |
| Sanskrit | ? | 50 | 1.611 |
| Santali | ? | 50 | 1.598 |
| Sindhi | ? | 50 | 1.479 |
| Tamil | ? | 50 | 1.311 |
| Telugu | ? | 50 | 1.168 |
| Urdu | ? | 50 | 0.974 |
| **macro, all (22)** |  | 50 | 1.346 |
| **macro, one script (18)** |  | 50 | 1.282 |

### Tokens per character (the scored references, no BOS; IndicTrans2: of its pre-processed reference, per character of the reference)

| language | characters per sentence | gemma-3-4b-it |
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
| gemma-int4@neutral | metal-int4 | 2.85 | 27.5 | 75 | 0.86 / 2.03 | 3.75 | 5.78 | 2200 | 153 |
| gemma-int4 | metal-int4 | 2.85 | 33.0 | 113 | 1.08 / 8.29 | 3.74 | 4.65 | 127 | 73 |

### Per-output diagnostics (the directions with any)

| config | direction | outputs | under 50% in the target's script (letters) | stopped by max_new_tokens | with special tokens (removed before scoring) | with other added tokens (kept) |
|---|---:|---:|---:|---:|---:|---:|
| gemma-int4@neutral | eng-asm | 50 | 10 | 4 | 0 | 0 |
| gemma-int4@neutral | eng-ben | 50 | 1 | 0 | 0 | 0 |
| gemma-int4@neutral | eng-brx | 50 | 49 | 22 | 0 | 0 |
| gemma-int4@neutral | eng-doi | 50 | 4 | 2 | 0 | 0 |
| gemma-int4@neutral | eng-gom | 50 | 48 | 1 | 0 | 0 |
| gemma-int4@neutral | eng-kan | 50 | 19 | 1 | 0 | 0 |
| gemma-int4@neutral | eng-kas | 50 | 7 | 18 | 0 | 0 |
| gemma-int4@neutral | eng-mai | 50 | 6 | 2 | 0 | 0 |
| gemma-int4@neutral | eng-mal | 50 | 22 | 3 | 0 | 0 |
| gemma-int4@neutral | eng-mni | 50 | 30 | 32 | 0 | 0 |
| gemma-int4@neutral | eng-npi | 50 | 2 | 0 | 0 | 0 |
| gemma-int4@neutral | eng-ory | 50 | 4 | 6 | 0 | 0 |
| gemma-int4@neutral | eng-san | 50 | 4 | 0 | 0 | 0 |
| gemma-int4@neutral | eng-sat | 50 | 50 | 4 | 0 | 0 |
| gemma-int4@neutral | eng-snd | 50 | 50 | 3 | 0 | 0 |
| gemma-int4@neutral | eng-tam | 50 | 1 | 0 | 0 | 0 |
| gemma-int4@neutral | eng-urd | 50 | 2 | 0 | 0 | 0 |
| gemma-int4@neutral | snd-eng | 50 | 1 | 0 | 0 | 0 |
| gemma-int4 | eng-asm | 3 | 3 | 0 | 0 | 0 |
| gemma-int4 | eng-ben | 3 | 3 | 1 | 0 | 0 |
| gemma-int4 | eng-brx | 3 | 3 | 2 | 0 | 0 |
| gemma-int4 | eng-doi | 3 | 3 | 0 | 0 | 0 |
| gemma-int4 | eng-gom | 3 | 3 | 2 | 0 | 0 |
| gemma-int4 | eng-guj | 3 | 3 | 1 | 0 | 0 |
| gemma-int4 | eng-hin | 3 | 3 | 0 | 0 | 0 |
| gemma-int4 | eng-kan | 3 | 3 | 1 | 0 | 0 |
| gemma-int4 | eng-kas | 3 | 2 | 2 | 0 | 0 |
| gemma-int4 | eng-mai | 3 | 3 | 1 | 0 | 0 |
| gemma-int4 | eng-mal | 3 | 3 | 1 | 0 | 0 |
| gemma-int4 | eng-mar | 3 | 3 | 1 | 0 | 0 |
| gemma-int4 | eng-mni | 3 | 3 | 2 | 0 | 0 |
| gemma-int4 | eng-npi | 3 | 3 | 0 | 0 | 0 |
| gemma-int4 | eng-ory | 3 | 3 | 1 | 0 | 0 |
| gemma-int4 | eng-pan | 3 | 3 | 2 | 0 | 0 |
| gemma-int4 | eng-san | 3 | 3 | 2 | 0 | 0 |
| gemma-int4 | eng-sat | 3 | 3 | 1 | 0 | 0 |
| gemma-int4 | eng-snd | 3 | 3 | 0 | 0 | 0 |
| gemma-int4 | eng-tam | 3 | 3 | 1 | 0 | 0 |
| gemma-int4 | eng-tel | 3 | 3 | 1 | 0 | 0 |
| gemma-int4 | eng-urd | 3 | 3 | 1 | 0 | 0 |

Scored references whose tokens decode to other text: gemma-int4@neutral 0 / 2200, gemma-int4 0 / 0 (IndicTrans2: of its pre-processed reference).
Code versions (git describe of this repo and the engine; SHA-256 of eval_translate.py with engine_run.py and the engine's src/, or with indictrans.py) per config: gemma-int4@neutral c0df389-dirty engine 324313a-dirty 626af229de5f2f07; gemma-int4 c0df389-dirty engine 324313a-dirty 626af229de5f2f07.

### Prompts (each through the model's own chat template; renderings in RUNS/CONFIG/meta.json)

- gemma-int4@neutral: `[{"role": "user", "content": "Translate the following text from {Source} to {Target}. Reply with the translation only.\n\n{text}"}]`
- gemma-int4: `[{"role": "system", "content": "Translate the text below to {Target}."}, {"role": "user", "content": "{text}"}]`
