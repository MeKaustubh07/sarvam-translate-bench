# Sarvam-Translate vs its base model vs IndicTrans2 on IN22-Gen

What does Sarvam AI's translation fine-tune of Gemma 3 4B add, and how does it compare with AI4Bharat's dedicated
Indic translator? All three run on one 8 GB MacBook Air (M2): Sarvam-Translate and Gemma 3 4B-it on a from-scratch
inference engine (Python, PyTorch, Metal kernels, calibrated INT4), IndicTrans2 1B through transformers on MPS.
An independent study, not affiliated with or endorsed by Sarvam AI, Google or AI4Bharat.

## Summary

- **Into Indic languages, Sarvam-Translate is the best of the three.** Macro chrF++ English→X: Sarvam 50.4,
  IndicTrans2 47.9 (−2.6 [−3.6, −1.5]), Gemma 3 4B-it 24.1. Sarvam is ahead of IndicTrans2 in 11 of 22 languages
  (the CI excludes zero) and behind in none. The largest gaps are in the rare scripts: Santali −8.2, Sindhi −7.2,
  Odia −7.0, Manipuri −6.0. COMET agrees: 79.9 vs 78.0 (−1.9 [−2.4, −1.3]).
- **Into English, IndicTrans2 is clearly the best.** Macro chrF++ X→English: IndicTrans2 62.5, Sarvam 52.2
  (+10.3 [+8.1, +12.4]), Gemma 47.7. IndicTrans2 is ahead in 21 of 22 languages. COMET shrinks the gap to
  +2.3 [+1.5, +3.1] (85.4 vs 83.1), which suggests that much of the chrF++ gap is wording, not meaning. IN22's
  English is the original text, which favours a literal system (see Threats).
- **The fine-tune mostly teaches the model to write Indic text.** Gemma 3 4B-it, the same architecture under the same
  quantization, is 26 chrF++ points behind Sarvam into Indic languages. Its outputs mix scripts and languages within a
  sentence, and it writes Bodo in Latin and Konkani mostly in Telugu script. Into English, Gemma is close: within
  0.5 COMET of Sarvam over XLM-R's 14 languages (−0.5 [−1.2, +0.2]). Its bits per character on the human reference
  are 4.6× Sarvam's into Indic languages and 2.5× into English.
- **The Gemma gap is not quantization.** On 10 ids, INT8 Gemma is within 1.3 chrF++ of INT4 Gemma (26.4 vs 25.1
  English→X), and INT8 Sarvam is within 0.1 of INT4 Sarvam.
- **The controls hold up.** Beam 5 adds +0.6 chrF++ to IndicTrans2 English→X and +0.5 X→English, so greedy decoding
  explains none of the X→English gap. Sarvam does not care which prompt it gets (−0.1 English→X). A rerun of
  200 Sarvam outputs with today's code was byte-identical, and an IndicTrans2 rerun reproduced 2,194 of 2,200 outputs
  (macro chrF++ within 0.1).

## Systems

| config | model | weights | how it runs |
|---|---|---|---|
| `sarvam-int4` (baseline) | Sarvam-Translate (`sarvamai/sarvam-translate`), Gemma 3 4B fine-tuned for translation | calibrated INT4, 2.99 GB | engine, Metal, continuous batching (8 in flight), greedy |
| `gemma-int4@neutral` | Gemma 3 4B-it (`google/gemma-3-4b-it`, rev `093f9f38`), the fine-tune's base | calibrated INT4, 2.85 GB | the same engine and settings |
| `indictrans2` | IndicTrans2 1B, one encoder-decoder per direction (`ai4bharat/indictrans2-{en-indic,indic-en}-1B`) | float16, 2.05 GB | transformers 4.57 remote code on MPS, batches of 8, greedy |

Controls, on subsets of the same ids: `sarvam-int8` and `gemma-int8@neutral` (INT8 weights), `indictrans2-beam5`
(beam search, as IndicTrans2's paper decodes), `sarvam-int4@neutral` and `gemma-int4` (each model under the other
prompt).

## Method

**Data.** IN22-Gen (revision `e042ab3d`, parquet SHA-256 pinned), 1,024 n-way parallel sentences written in English and
translated by professionals into the 22 languages. A seeded sample stratified by domain and source: 50 ids, the same
ids in every language and both directions, 44 directions, 2,200 outputs per system. Each language in IN22's own
script: Manipuri in Meitei Mayek, Santali in Ol Chiki, Sindhi in Devanagari, Kashmiri in Perso-Arabic.

**Prompts.** Sarvam-Translate gets its model card's prompt: system `Translate the text below to {Target}.`, the text as
the user turn, through Gemma 3's chat template. Gemma 3 4B-it was meant to get exactly the same prompt, so that the
comparison isolates the fine-tune. It does not work: under the card prompt the base model behaves as a chat assistant,
with preambles, numbered alternatives and word-by-word breakdowns. Its outputs averaged 423 tokens, and 13 of 49 in
English→Assamese ran to the length cap. That would measure instruction following, not translation, and would have
taken ~8 h. Gemma's headline therefore uses a neutral user turn: `Translate the following text from {Source} to
{Target}. Reply with the translation only.`. For the four languages written in more than one script, the
language name includes the script, e.g. "Manipuri (Meitei Mayek script)"; the other three are Santali, Sindhi and
Kashmiri. Both cross-prompt controls are run: Sarvam under the neutral prompt (10 ids) and Gemma under the card
prompt (3 ids). IndicTrans2 takes no prompt. IndicTransToolkit's IndicProcessor writes its FLORES-200 language tags,
normalises and transliterates as the model was trained, and post-processes the output.

**Decoding.** Greedy for all three. The length cap is 32 + 4 × (source characters) new tokens; IndicTrans2 is also
limited by its 256 positions. IndicTrans2's paper and card use beam 5, so a beam-5 control runs on 10 ids. Greedy is
the main setting because it is the only decoding the engine's batched scheduler shares across systems, and because it
costs the same per output token everywhere.

**Quantization.** Both 4B models use the engine's calibrated INT4. Every tensor group is INT4 except
the groups a rule keeps in INT8: the rule ranks groups by KL to fp32 saved per extra byte, measured on a calibration
set of 88 translation prompts. The policy was calibrated for each model separately. Sarvam-Translate was calibrated on
its own continuations; Gemma reused the same prompts and continuations.

| KL to fp32 (calib / held-out) | INT8 | flat INT4 | calibrated INT4 |
|---|---:|---:|---:|
| Sarvam-Translate | 0.00031 / 0.00038 | 0.0488 / 0.0607 | 0.0281 / 0.0394 (48 groups INT8, +271 MB) |
| Gemma 3 4B-it | 0.00205 / 0.00357 | 0.318 / 0.355 | 0.245 / 0.287 (24 groups INT8, +126 MB) |

On this text the base model loses 6.5× more to flat INT4 than the fine-tune. Its worst held-out languages are
Maithili (0.693 → 0.440 with the policy), Sindhi (0.671 → 0.425) and Odia (0.476 → 0.378). Part of the gap comes from
the calibration text: Sarvam's continuations are on the fine-tune's distribution, not the base model's. INT8
controls for both models (10 ids) measure how much of the gap is quantization. For Gemma it turns out to be little
(see Controls).

**IndicTrans2 on MPS.** float16 on MPS was checked against float32 on the CPU (`parity`): 64/64 greedy outputs equal,
max |Δ log p| 1.9e-2.

**chrF++.** sacrebleu 2.6.0, `nrefs:1|case:mixed|eff:yes|nc:6|nw:2|space:no`, corpus level over the 50 ids, on IN22's
own protocol (IndicTrans2's `compute_metrics.sh`): Indic targets go through IndicNLP normalize and trivial_tokenize,
English is scored raw.

**COMET.** `Unbabel/wmt22-comet-da` (revision `2760a223`, checkpoint SHA-256 `e213091c…`, unbabel-comet 2.2.7), CPU.
The scale is the mean segment score × 100. IndicCOMET (AI4Bharat's COMET fine-tuned on Indic MQM data) was the
first choice but could not be used: it is not on the Hugging Face Hub, it has no licence file, its object-store link
returns 403, and it was trained on English→5 languages only. wmt22-comet-da's XLM-R encoder covers 14 of the 22
languages as IN22 writes them (as, bn, gu, hi, kn, ml, mr, ne, or, pa, sa, ta, te, ur). The tables give a macro over
those 14 next to the all-language macro. Sindhi is left out of the 14: XLM-R's Sindhi is Perso-Arabic, IN22's is
Devanagari. COMET on the other eight languages is reported, but it is a score from an encoder that has not seen them.

**Confidence intervals.** Paired bootstrap against `sarvam-int4`: 95%, 1,000 resamples of the 50 ids, seed 0. A macro
row resamples ids jointly across its languages, because IN22 is n-way parallel and the languages share sentences.

**Bits per character.** The teacher-forced cost of the human reference given the prompt, in bits, divided by the
reference's characters. Because it is per character, it compares across tokenizers. It is reported without and with
the end of the answer (the probability of any stop token). Sarvam's bits are conditioned on its card prompt and
Gemma's on the neutral one. IndicTrans2's cost is of IndicProcessor's pre-processed reference: normalised, tokenised,
and in most scripts transliterated to Devanagari. That is a different text, so its bits are reported separately and
are not comparable.

**Tokens per character** of the references, through each model's tokenizer.

## Results

Full per-language tables, including bits per character with the end-of-answer token and the per-output diagnostics,
are in `results/tables.md`. CIs are paired bootstrap 95% against `sarvam-int4`.

### Macro scores (50 ids, 22 languages)

| metric | direction | sarvam-int4 | gemma-int4@neutral | indictrans2 |
|---|---|---:|---:|---:|
| chrF++ | English→X | 50.4 | 24.1 (−26.4 [−27.9, −24.8]) | 47.9 (−2.6 [−3.6, −1.5]) |
| chrF++ | X→English | 52.2 | 47.7 (−4.5 [−7.1, −2.4]) | 62.5 (+10.3 [+8.1, +12.4]) |
| COMET | English→X | 79.9 | 62.0 (−17.9 [−18.8, −17.1]) | 78.0 (−1.9 [−2.4, −1.3]) |
| COMET | X→English | 83.1 | 77.8 (−5.3 [−6.2, −4.5]) | 85.4 (+2.3 [+1.5, +3.1]) |
| COMET, XLM-R's 14 | English→X | 85.4 | 73.4 (−12.0 [−13.0, −11.0]) | 84.0 (−1.4 [−2.0, −0.9]) |
| COMET, XLM-R's 14 | X→English | 86.3 | 85.8 (−0.5 [−1.2, +0.2]) | 88.7 (+2.4 [+1.7, +3.1]) |
| bits / char | English→X | 0.636 | 2.917 | not comparable |
| bits / char | X→English | 0.529 | 1.343 | not comparable |

The 18-language macro without the multi-script languages tells the same story: chrF++ English→X 52.0 / 28.8 /
50.2, X→English 53.6 / 51.5 / 64.3.

### Sarvam-Translate vs IndicTrans2

Into Indic languages, the CI excludes zero in 11 languages, all in Sarvam's favour; the other 11 are within noise.
IndicTrans2 has no significant win; the nearest is Nepali (+4.4 [−3.8, +14.4]), where one Sarvam runaway output
widens the CI. Into English, IndicTrans2 leads in 21 of 22 languages, by about 10 points in most. The exception is
Santali (+1.6 n.s.). COMET X→English has IndicTrans2 ahead in 19 of 22, by a margin about a quarter of chrF++'s.
The outputs show no failure mode behind the X→English gap. Length ratios are about 0.96 to 1.0 for both systems and
no output runs to several lines. Sarvam paraphrases more and IndicTrans2 stays closer to the source's wording, which
is what a reference translated from English rewards.

### Rare scripts

English→X, chrF++:

| language (IN22 script) | sarvam-int4 | indictrans2 | gemma-int4@neutral |
|---|---:|---:|---:|
| Manipuri (Meitei Mayek) | 50.0 | 44.0 (−6.0 [−8.8, −3.5]) | 2.0 |
| Santali (Ol Chiki) | 39.7 | 31.5 (−8.2 [−10.4, −6.1]) | 1.1 |
| Sindhi (Devanagari) | 41.7 | 34.4 (−7.2 [−10.2, −4.0]) | 1.8 |
| Kashmiri (Perso-Arabic) | 42.8 | 39.8 (−2.9 [−4.5, −1.2]) | 5.4 |
| Odia | 50.6 | 43.6 (−7.0 [−8.9, −5.1]) | 16.4 |

Sarvam's largest leads over IndicTrans2 are in these five, although IN22 follows IndicTrans2's script conventions.
Gemma barely writes these scripts at all. It writes Sindhi in Perso-Arabic (48 of 50), which is a legitimate
convention but not IN22's, and Santali in Bengali script (44 of 50). Its Manipuri is split between Meitei Mayek (20)
and Ol Chiki (15), and 32 of its 50 Manipuri outputs loop to the length cap. COMET on Manipuri, Santali and Sindhi
is not reliable, because XLM-R has not seen them: it gives Sarvam's Santali 88.7.

### Tokens per character

Sarvam-Translate and Gemma share Gemma 3's tokenizer, and the fine-tune did not change it. Per reference character:
Manipuri 1.830 tokens (IndicTrans2 0.334), Santali 1.016 (0.284), Odia 0.730 (0.250), Kashmiri 0.570 (0.293).
Hindi is 0.281 (0.250) and English 0.214 (0.221). In Meitei Mayek, Gemma 3's tokenizer is close to byte level, so a
Manipuri output costs 5.5× IndicTrans2's tokens and 6.5× Hindi's. IndicTrans2's numbers are of its pre-processed
text: most scripts are transliterated to Devanagari before its SentencePiece model.

### Speed and memory

One M2 MacBook Air, 8 GB, nothing else on the GPU; greedy; the stacks differ (see the caveats in `results/tables.md`).

| config | stack | output tok/s | output chars/s | TTFT p50 / p90 (s) | peak GPU (GiB) | outputs timed |
|---|---|---:|---:|---:|---:|---:|
| sarvam-int4 | engine, Metal INT4, 8 in flight | 21.0 | 59 | 1.02 / 1.83 | 4.52 | 2,136 |
| gemma-int4@neutral | the same | 27.5 | 75 | 0.86 / 2.03 | 3.75 | 2,200 |
| indictrans2 (`results/control-speed`) | transformers, MPS fp16, batches of 8 | 127.0 | 518 | 0.24 / 0.49 | 5.15 | 2,200 |

IndicTrans2 is about 9× faster per output character. It is a 1B encoder-decoder, and a direction's encoder runs once
per batch. Sarvam's and Gemma's 4B decoders spend 2 to 5.5× more tokens per character in the rare scripts. Gemma's
higher token rate than Sarvam's is not attributed: Sarvam's run was made over several sessions by earlier engine
versions. IndicTrans2's
peak GPU memory holds both directions' models in one process.

## Controls

All on the first 10 (or 3) ids of the same seeded sample. CIs are against the control's own baseline; each control
report is in `results/control-*/`.

| control | ids | chrF++ English→X | chrF++ X→English | COMET English→X | COMET X→English |
|---|---:|---:|---:|---:|---:|
| `sarvam-int8` vs `sarvam-int4` | 10 | 53.0 vs 53.1 (−0.1 [−0.6, +0.2]) | 55.5 vs 53.8 (+1.7 [−0.4, +2.8]) | 81.4 vs 81.6 | 84.4 vs 84.3 |
| `gemma-int8@neutral` vs `gemma-int4@neutral` | 10 | 26.4 vs 25.1 | 50.1 vs 49.6 | 63.9 vs 64.1 | 79.7 vs 79.4 |
| `indictrans2-beam5` vs `indictrans2` | 10 | 51.7 vs 51.0 (+0.6 [+0.2, +1.5]) | 68.0 vs 67.5 (+0.5 [−0.3, +1.3]) | 80.3 vs 79.9 | 86.6 vs 86.6 |
| `sarvam-int4@neutral` vs `sarvam-int4` | 10 | 53.0 vs 53.1 (−0.1 [−0.7, +0.3]) | 54.2 vs 53.8 (+0.4 [−3.8, +3.6]) | 81.5 vs 81.6 | 81.6 vs 84.3 (−2.7 [−5.3, −0.6]) |
| `gemma-int4` (card) vs `gemma-int4@neutral` | 3 | 11.7 vs 26.9 (−15.2 [−18.0, −11.7]) | 41.0 vs 51.8 (−10.8 [−15.0, −4.5]) | 36.7 vs 65.2 | 67.3 vs 81.0 |

- **Quantization.** INT4 costs Sarvam nothing measurable into Indic languages. Its INT8 X→English gain (+1.7) is inside the
  CI. For Gemma, INT8 and INT4 differ by under 1.5 points, and INT8 outputs
  mix scripts as often (English→Kannada: 10 of 10 at INT8, 9 of 10 at INT4). Gemma's weakness is the model's own.
- **Beam 5.** About half a chrF++ point for IndicTrans2 in each direction. The paper's beam 5 would widen its
  X→English lead slightly and narrow its English→X deficit slightly; neither conclusion changes.
- **Prompt.** Sarvam ignores the prompt's wording into Indic languages, including the script naming. Its X→English
  COMET drop under the neutral prompt is in the multi-script source languages (the 18-language macro is −0.1). Gemma
  under Sarvam's card prompt answers as a chat assistant, so the neutral prompt is the fair one for it.
- **Determinism.** Sarvam INT4: 200 of 200 outputs (Hindi and Manipuri, both directions) byte-identical to the main
  run, which was made by three earlier code versions. IndicTrans2 on MPS: a full rerun matched 2,194 of 2,200
  outputs, with macro chrF++ 47.9 and 62.6 vs 47.9 and 62.5. The 6 that differ are all X→English: float16 on MPS is not bit-reproducible.

## Threats to validity

- **IN22 and IndicTrans2 share authors.** AI4Bharat built both, so IN22-Gen's translation conventions (style,
  transliteration of names, Manipuri in Meitei Mayek, Santali in Ol Chiki, Sindhi in Devanagari) are IndicTrans2's
  training conventions. Sarvam-Translate and Gemma were trained on other conventions. An output in another valid
  convention loses chrF++, and IndicTrans2 may gain most where the conventions are least shared (the rare scripts).
- **English is the original.** IN22-Gen was written in English and translated into the Indic languages. So X→English
  asks a model to recover English that a human translation came from. A literal system has the advantage there, and
  IndicTrans2 is more literal than Sarvam-Translate, which paraphrases more. Part of IndicTrans2's ~10-point X→English
  lead may be this effect.
- **Greedy, not beam 5.** IndicTrans2's published numbers use beam 5. The beam-5 control puts what greedy costs it
  at about half a chrF++ point, on 10 ids.
- **50 sentences per language.** The bootstrap CIs show the noise, but they are CIs over these 1,024 sentences' domains,
  not over Indic text in general. Single-language differences of 1 to 2 points are mostly inside them.
- **Runaway outputs.** chrF++ is computed at corpus level, so one runaway output (a loop to the length cap) changes a
  direction's score by several points. Sarvam has 7 in 2,200 outputs. One each in Assamese→English and
  Kashmiri→English (7,079 and 5,679 characters against references of 343 and 463) explains most of its low scores
  there. The per-output diagnostics in `results/tables.md` list them.
- **COMET's coverage.** XLM-R has not seen 8 of the 22 languages in IN22's scripts, and COMET models are known to
  reward fluent English. COMET is a second opinion on the 14, not a verdict on the other eight.
- **Gemma's INT4 loses more than Sarvam's.** Its KL is 6 to 9× Sarvam's. The INT8 control on 10 ids bounds the
  effect: INT8 Gemma is within 1.5 chrF++ points of INT4 Gemma in both directions, and it mixes scripts just as
  much. INT8 itself is 0.002 KL from transformers' own fp32 layers on the calibration prompts, so the engine is not
  the cause.
- **The neutral prompt names the script.** That may help Gemma on Manipuri, Santali, Sindhi and Kashmiri more than Sarvam's card
  prompt helps Sarvam. The Sarvam neutral control found no effect into Indic languages (−0.1), so the
  prompts compare fairly where it matters most.
- **Speed** comes from one run per config on one laptop, with different stacks and tokenizers. IndicTrans2's main run
  only recorded speed for its last 260 outputs, so the speed numbers come from a full rerun (`results/control-speed`).
  Sarvam's speed covers the 2,136 outputs generated after speed logging existed.

## Reproduce

See the README. Every number here is in `results/` (`tables.md`, `numbers.json`, `numbers.csv`, `chrf.svg`) and the
control reports in `results/control-*/`; scores and sentence ids only, no dataset text or model outputs.
