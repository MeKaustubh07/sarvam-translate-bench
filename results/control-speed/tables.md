chrF++: sacrebleu `nrefs:1|case:mixed|eff:yes|nc:6|nw:2|space:no|version:2.6.0`, corpus level over the sampled ids, on IN22's protocol (IN22-Gen / IndicTrans2 compute_metrics.sh: Indic targets IndicNLP normalize (default options) + trivial_tokenize, English raw; indic-nlp-library 0.92, urduhack 1.1.1). In brackets: the difference from indictrans2 and its paired bootstrap 95% CI (1000 resamples, seed 0; a macro row resamples the shared ids jointly over its languages). Support claimed by indictrans2. Macro rows: all languages; one script (without Manipuri, Sindhi, Kashmiri, Santali, written in more than one); a config without every language of a row shows -.

Bits per character compare models that score the reference itself: none. 

### chrF++ (higher is better), English -> X

| language | support | n | indictrans2 |
|---|---:|---:|---:|
| Assamese | yes | 50 | 45.4 |
| Bengali | yes | 50 | 52.3 |
| Bodo | yes | 50 | 48.5 |
| Dogri | yes | 50 | 56.9 |
| Konkani | yes | 50 | 44.5 |
| Gujarati | yes | 50 | 53.2 |
| Hindi | yes | 50 | 53.4 |
| Kannada | yes | 50 | 50.5 |
| Kashmiri | yes | 50 | 39.8 |
| Maithili | yes | 50 | 47.3 |
| Malayalam | yes | 50 | 53.2 |
| Marathi | yes | 50 | 52.3 |
| Manipuri | yes | 50 | 44.0 |
| Nepali | yes | 50 | 50.2 |
| Odia | yes | 50 | 43.6 |
| Punjabi | yes | 50 | 46.1 |
| Sanskrit | yes | 50 | 37.4 |
| Santali | yes | 50 | 31.5 |
| Sindhi | yes | 50 | 34.4 |
| Tamil | yes | 50 | 50.6 |
| Telugu | yes | 50 | 51.7 |
| Urdu | yes | 50 | 66.7 |
| **macro, all (22)** |  | 50 | 47.9 |
| **macro, one script (18)** |  | 50 | 50.2 |

### chrF++ (higher is better), X -> English

| language | support | n | indictrans2 |
|---|---:|---:|---:|
| Assamese | yes | 50 | 65.3 |
| Bengali | yes | 50 | 64.3 |
| Bodo | yes | 50 | 62.4 |
| Dogri | yes | 50 | 72.2 |
| Konkani | yes | 50 | 58.1 |
| Gujarati | yes | 50 | 67.3 |
| Hindi | yes | 50 | 61.0 |
| Kannada | yes | 50 | 64.8 |
| Kashmiri | yes | 50 | 58.2 |
| Maithili | yes | 50 | 65.0 |
| Malayalam | yes | 50 | 65.3 |
| Marathi | yes | 50 | 64.6 |
| Manipuri | yes | 50 | 60.6 |
| Nepali | yes | 50 | 70.0 |
| Odia | yes | 50 | 66.1 |
| Punjabi | yes | 50 | 59.7 |
| Sanskrit | yes | 50 | 55.7 |
| Santali | yes | 50 | 44.2 |
| Sindhi | yes | 50 | 55.1 |
| Tamil | yes | 50 | 60.1 |
| Telugu | yes | 50 | 65.3 |
| Urdu | yes | 50 | 71.0 |
| **macro, all (22)** |  | 50 | 62.6 |
| **macro, one script (18)** |  | 50 | 64.3 |

### Tokens per character (the scored references, no BOS; IndicTrans2: of its pre-processed reference, per character of the reference)

| language | characters per sentence | indictrans2 |
|---|---:|---:|

### Speed and memory (generation: greedy)

Not a like-for-like race: engine configs run this repo's sibling engine (Metal INT8/INT4 kernels, continuous batching: a closed loop of `batch` requests in flight); IndicTrans2 runs eager PyTorch through transformers' remote code (static batches of `batch` sources sorted by length, finished rows padded until the batch ends, the encoder run once per batch). Tokens are each model's own (tokens per character below differ), so compare output characters per second. TTFT: from a request's arrival in the engine's queue; for IndicTrans2, from its batch's start (tokenising and the encoder included). One run on one M2 MacBook Air (8 GB), nothing else on the GPU.

| config | stack | weights (GB) | output tok/s | output chars/s | TTFT p50 / p90 (s) | peak GPU (GiB) | peak footprint (GiB) | requests | preempted |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| indictrans2 | hf mps float16 | 2.05 | 127.0 | 518 | 0.24 / 0.49 | 5.15 | 6.51 | 2200 | 0 |

### Per-output diagnostics (the directions with any)

none

Scored references whose tokens decode to other text: indictrans2 0 / 0 (IndicTrans2: of its pre-processed reference).
Code versions (git describe of this repo and the engine; SHA-256 of eval_translate.py with engine_run.py and the engine's src/, or with indictrans.py) per config: indictrans2 c0df389-dirty b9870acb3fb415a5.

### Prompts (each through the model's own chat template; renderings in RUNS/CONFIG/meta.json)

- indictrans2: none: IndicProcessor's language tags (`eng_Latn mni_Mtei TEXT`)
