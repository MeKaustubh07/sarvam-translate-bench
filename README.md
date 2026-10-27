# Indic translation bench

How well three openly available translation models translate into and out of the 22 scheduled Indian languages on
IN22-Gen, measured on one 8 GB MacBook Air (M2):

| config | model | how it runs |
|---|---|---|
| `sarvam-int4`, `sarvam-int8` | Sarvam-Translate (`sarvamai/sarvam-translate`, Gemma 3 4B fine-tuned for translation) | [InferenceEngine](../InferenceEngine), Metal INT4 (calibrated policy) / INT8 |
| `gemma-int4`, `gemma-int8` | Gemma 3 4B-it (`google/gemma-3-4b-it`), the model Sarvam-Translate was fine-tuned from | the same engine, the same quantization |
| `indictrans2` | IndicTrans2 1B (`ai4bharat/indictrans2-en-indic-1B`, `ai4bharat/indictrans2-indic-en-1B`), encoder-decoder | transformers with its remote code, IndicTransToolkit's IndicProcessor |

Gemma 3 4B-it gets exactly Sarvam-Translate's prompt, so `gemma-*` vs `sarvam-*` isolates what the translation
fine-tune adds to the same architecture, size and quantization. IndicTrans2 is the dedicated translation model built
by AI4Bharat, IN22-Gen's authors.

An independent study: not affiliated with or endorsed by Sarvam AI, Google or AI4Bharat.

## Method

- **Data:** IN22-Gen (`ai4bharat/IN22-Gen`, revision `e042ab3d`, parquet SHA-256 pinned in `scripts/eval_translate.py`;
  evaluation only). A seeded, domain x source stratified sample of its 1,024 sentences (`--n`, default 50 for
  generation), the same ids in every language and direction; every language in IN22's own script (Manipuri in Meitei
  Mayek, Santali in Ol Chiki, Sindhi in Devanagari, Kashmiri in Perso-Arabic). 44 directions.
- **Prompts:** Sarvam-Translate and Gemma 3: the Sarvam card's, system `Translate the text below to {Target}.` and the
  text as the user turn, through each model's own chat template (Gemma 3's folds the system turn into the first user
  turn). `--prompt neutral` is a control (a user turn naming both languages and the script). IndicTrans2: no prompt;
  IndicProcessor writes the FLORES-200 tags (`eng_Latn mni_Mtei ...`, the same codes as IN22-Gen's columns), normalises
  and transliterates as IndicTrans2 was trained, and post-processes the output. Every run's `meta.json` records its
  prompt and a rendering.
- **Decoding:** greedy everywhere (IndicTrans2 `num_beams=1`, not its card's beam 5), at most 32 + 4 x (source
  characters) new tokens (IndicTrans2 also at most its 256 positions).
- **chrF++:** sacrebleu `nrefs:1|case:mixed|eff:yes|nc:6|nw:2|space:no|version:2.6.0`, corpus level, on IN22's protocol
  (IndicTrans2 `compute_metrics.sh`: Indic targets through IndicNLP normalize + trivial_tokenize, English raw).
- **CIs:** paired bootstrap against `sarvam-int4`, 95%, 1,000 resamples; a macro row resamples the shared ids jointly
  over its languages (IN22 is n-way parallel, so languages are correlated).
- **Bits per character:** teacher-forced cost of the human reference given the prompt, in bits, over the reference's
  characters (comparable across tokenizers), without and with the end of answer (the probability of any stop token).
  IndicTrans2 is scored the same way, but on IndicProcessor's pre-processed reference (normalised, tokenised, most
  scripts transliterated to Devanagari) through its SentencePiece models: another text, so its bits are reported apart
  and marked not comparable.
- **Tokens per character** of the references through each model's tokenizer (IndicTrans2's of its pre-processed text).
- **Speed:** recorded per run, with the caveats printed above the table: different stacks (the engine's Metal kernels
  and continuous batching vs eager PyTorch in static batches), different tokenizers; compare output characters per
  second.

The earlier version of this study (Sarvam-Translate vs Tiny Aya Global and Qwen3.5-2B) is in the engine's history at
commit `9eaa6eb` (`docs/bench/sarvam-translate.md`); its Sarvam runs are reused here (`runs/sarvam-int4`,
`runs/sarvam-int8`).

## Layout

- `scripts/eval_translate.py`: data, sampling, prompts, engine generation and scoring, the CLI.
- `scripts/indictrans.py`: the IndicTrans2 backend (generate, score, `parity`).
- `scripts/eval_translate_report.py`: chrF++, bootstrap, tables and chart.
- `data/` (gitignored): `in22-gen/` (the dataset and its manifest), `models/` (IndicTrans2's checkpoints).
- `runs/` (gitignored): every config's outputs, scores, speed and code versions; resumable.
- `results/`: `tables.md`, `numbers.json`, `numbers.csv`, `chrf.svg`; scores only, no dataset text or model outputs.

## Reproduce

The engine is a sibling checkout (`../InferenceEngine`, or set `ENGINE`); engine configs and the report run in its
venv with `requirements.txt` added. IndicTrans2's remote code is written for transformers 4, so it runs in a venv of
its own (`requirements-indictrans2.txt`, which says how to make it).

```bash
E=../InferenceEngine/scripts/.venv/bin/python       # engine configs, the report, the tests
I=.venv-it2/bin/python                               # indictrans2
$E scripts/eval_translate.py data                    # IN22-Gen (gated: accept its terms) -> data/in22-gen/
$E scripts/eval_translate.py generate sarvam-int4    # per engine config; resumes where a run stopped
$E scripts/eval_translate.py score sarvam-int4 --n 50
$I scripts/eval_translate.py parity                  # IndicTrans2 on MPS float16 vs CPU float32
$I scripts/eval_translate.py generate indictrans2    # --device / --dtype as parity allows
$I scripts/eval_translate.py score indictrans2 --n 50
$E scripts/eval_translate.py report
$E tests/test_eval_translate.py                      # tiny random models only; runs the IndicTrans2 suite in $I
```

## Licences and attribution

- Code: Apache-2.0 (`LICENSE`).
- IN22-Gen: CC-BY-4.0, AI4Bharat (Gala et al., 2023, "IndicTrans2", TMLR). Not redistributed here.
- Sarvam-Translate: Sarvam AI; its model card tags gpl-3.0, and as a Gemma 3 derivative it is also under Google's
  Gemma Terms of Use.
- Gemma 3: Google, Gemma Terms of Use (https://ai.google.dev/gemma/terms).
- IndicTrans2 and IndicTransToolkit: AI4Bharat, MIT.
- No weights are redistributed; the scripts download nothing but the dataset.
