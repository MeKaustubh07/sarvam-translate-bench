chrF++: sacrebleu `nrefs:1|case:mixed|eff:yes|nc:6|nw:2|space:no|version:2.6.0`, corpus level over the sampled ids, on IN22's protocol (IN22-Gen / IndicTrans2 compute_metrics.sh: Indic targets IndicNLP normalize (default options) + trivial_tokenize, English raw; indic-nlp-library 0.92, urduhack 1.1.1). In brackets: the difference from sarvam-int4 and its paired bootstrap 95% CI (1000 resamples, seed 0; a macro row resamples the shared ids jointly over its languages). Support claimed by sarvam-translate / gemma-3-4b-it / indictrans2. Macro rows: all languages; one script (without Manipuri, Sindhi, Kashmiri, Santali, written in more than one); a config without every language of a row shows -.

COMET: Unbabel/wmt22-comet-da (revision 2760a223, unbabel-comet 2.2.7), reference-based, raw text (no IN22 normalisation), on the CPU. Its encoder (XLM-R) never saw Bodo, Dogri, Konkani, Kashmiri, Maithili, Manipuri, Santali, Sindhi: their COMET is not reliable; the macro over XLM-R's languages leaves them out.

Bits per character compare models that score the reference itself: sarvam-int4, sarvam-int8, gemma-int4@neutral. indictrans2 score IndicProcessor's pre-processed reference, reported apart.

### chrF++ (higher is better), English -> X

| language | support | n | sarvam-int4 | gemma-int4@neutral | indictrans2 |
|---|---:|---:|---:|---:|---:|
| Assamese | yes / ? / yes | 50 | 48.3 | 19.1 (-29.2 [-33.5, -24.9]) | 45.4 (-2.9 [-5.3, -0.7]) |
| Bengali | yes / ? / yes | 50 | 54.5 | 42.3 (-12.2 [-15.3, -9.2]) | 52.3 (-2.2 [-4.2, -0.4]) |
| Bodo | yes / ? / yes | 50 | 49.8 | 1.5 (-48.3 [-52.0, -44.6]) | 48.5 (-1.3 [-4.5, +2.4]) |
| Dogri | yes / ? / yes | 50 | 59.5 | 22.1 (-37.4 [-42.4, -32.6]) | 56.9 (-2.6 [-5.2, -0.2]) |
| Konkani | yes / ? / yes | 50 | 46.2 | 3.9 (-42.3 [-45.6, -38.9]) | 44.5 (-1.7 [-3.6, +0.3]) |
| Gujarati | yes / ? / yes | 50 | 54.3 | 43.3 (-11.0 [-13.4, -8.6]) | 53.2 (-1.1 [-3.2, +1.0]) |
| Hindi | yes / ? / yes | 50 | 55.6 | 49.0 (-6.6 [-9.7, -3.5]) | 53.4 (-2.2 [-4.4, -0.0]) |
| Kannada | yes / ? / yes | 50 | 55.2 | 18.9 (-36.4 [-41.5, -30.4]) | 50.5 (-4.7 [-7.0, -2.4]) |
| Kashmiri | yes / ? / yes | 50 | 42.8 | 5.4 (-37.4 [-40.8, -34.0]) | 39.8 (-2.9 [-4.5, -1.2]) |
| Maithili | yes / ? / yes | 50 | 50.4 | 25.5 (-24.9 [-28.6, -21.5]) | 47.3 (-3.1 [-5.1, -1.2]) |
| Malayalam | yes / ? / yes | 50 | 54.8 | 14.1 (-40.7 [-45.8, -34.0]) | 53.2 (-1.6 [-3.9, +0.9]) |
| Marathi | yes / ? / yes | 50 | 53.4 | 42.1 (-11.4 [-14.9, -8.2]) | 52.3 (-1.1 [-3.7, +1.3]) |
| Manipuri | yes / ? / yes | 50 | 50.0 | 2.0 (-48.0 [-51.5, -44.6]) | 44.0 (-6.0 [-8.8, -3.5]) |
| Nepali | yes / ? / yes | 50 | 45.7 | 37.3 (-8.4 [-17.4, +2.9]) | 50.2 (+4.4 [-3.8, +14.4]) |
| Odia | yes / ? / yes | 50 | 50.6 | 16.4 (-34.1 [-38.1, -30.3]) | 43.6 (-7.0 [-8.9, -5.1]) |
| Punjabi | yes / ? / yes | 50 | 46.7 | 32.4 (-14.3 [-18.4, -10.6]) | 46.1 (-0.6 [-2.5, +1.5]) |
| Sanskrit | yes / ? / yes | 50 | 41.6 | 21.2 (-20.4 [-23.9, -16.9]) | 37.4 (-4.2 [-7.4, -1.0]) |
| Santali | yes / ? / yes | 50 | 39.7 | 1.1 (-38.6 [-42.1, -34.8]) | 31.5 (-8.2 [-10.4, -6.1]) |
| Sindhi | yes / ? / yes | 50 | 41.7 | 1.8 (-39.8 [-43.8, -35.9]) | 34.4 (-7.2 [-10.2, -4.0]) |
| Tamil | yes / ? / yes | 50 | 52.5 | 44.9 (-7.7 [-10.3, -5.2]) | 50.6 (-1.9 [-3.8, +0.0]) |
| Telugu | yes / ? / yes | 50 | 51.6 | 44.0 (-7.7 [-9.8, -5.4]) | 51.7 (+0.1 [-1.8, +1.5]) |
| Urdu | yes / ? / yes | 50 | 64.8 | 41.2 (-23.5 [-28.2, -19.2]) | 66.7 (+2.0 [-0.6, +4.7]) |
| **macro, all (22)** |  | 50 | 50.4 | 24.1 (-26.4 [-27.9, -24.8]) | 47.9 (-2.6 [-3.6, -1.5]) |
| **macro, one script (18)** |  | 50 | 52.0 | 28.8 (-23.1 [-24.8, -21.5]) | 50.2 (-1.8 [-2.8, -0.7]) |

### chrF++ (higher is better), X -> English

| language | support | n | sarvam-int4 | gemma-int4@neutral | indictrans2 |
|---|---:|---:|---:|---:|---:|
| Assamese | yes / ? / yes | 50 | 45.1 | 52.3 (+7.2 [-4.3, +19.3]) | 65.3 (+20.1 [+8.8, +33.3]) |
| Bengali | yes / ? / yes | 50 | 55.0 | 55.7 (+0.7 [-2.5, +4.2]) | 64.3 (+9.3 [+6.0, +13.2]) |
| Bodo | yes / ? / yes | 50 | 50.9 | 27.2 (-23.7 [-27.9, -19.6]) | 62.4 (+11.5 [+8.2, +15.0]) |
| Dogri | yes / ? / yes | 50 | 56.3 | 44.7 (-11.6 [-15.5, -8.0]) | 72.2 (+15.9 [+12.7, +19.2]) |
| Konkani | yes / ? / yes | 50 | 50.5 | 44.4 (-6.1 [-9.0, -3.0]) | 58.1 (+7.5 [+4.0, +11.4]) |
| Gujarati | yes / ? / yes | 50 | 55.9 | 57.9 (+2.0 [-2.0, +6.1]) | 67.3 (+11.4 [+7.5, +15.5]) |
| Hindi | yes / ? / yes | 50 | 54.7 | 55.9 (+1.2 [-1.7, +4.1]) | 61.0 (+6.3 [+2.8, +9.6]) |
| Kannada | yes / ? / yes | 50 | 53.0 | 53.6 (+0.7 [-2.4, +3.4]) | 64.8 (+11.9 [+8.3, +15.3]) |
| Kashmiri | yes / ? / yes | 50 | 43.7 | 36.1 (-7.7 [-18.8, +3.7]) | 58.2 (+14.5 [+5.6, +22.8]) |
| Maithili | yes / ? / yes | 50 | 54.6 | 52.5 (-2.1 [-4.9, +1.1]) | 65.0 (+10.4 [+7.2, +14.2]) |
| Malayalam | yes / ? / yes | 50 | 54.3 | 53.8 (-0.5 [-3.5, +3.1]) | 65.0 (+10.7 [+7.3, +14.4]) |
| Marathi | yes / ? / yes | 50 | 54.0 | 56.5 (+2.5 [-0.2, +5.1]) | 64.6 (+10.6 [+7.6, +13.8]) |
| Manipuri | yes / ? / yes | 50 | 50.2 | 20.5 (-29.7 [-35.0, -24.4]) | 60.6 (+10.3 [+6.6, +13.9]) |
| Nepali | yes / ? / yes | 50 | 60.1 | 58.7 (-1.4 [-4.4, +1.6]) | 70.0 (+9.9 [+6.0, +13.9]) |
| Odia | yes / ? / yes | 50 | 55.3 | 49.1 (-6.2 [-10.1, -2.2]) | 66.1 (+10.8 [+7.4, +14.4]) |
| Punjabi | yes / ? / yes | 50 | 50.0 | 52.1 (+2.0 [-1.0, +5.5]) | 59.7 (+9.7 [+5.7, +14.2]) |
| Sanskrit | yes / ? / yes | 50 | 50.0 | 41.4 (-8.6 [-12.3, -4.7]) | 55.7 (+5.7 [+2.7, +9.2]) |
| Santali | yes / ? / yes | 50 | 42.7 | 29.4 (-13.3 [-16.5, -10.4]) | 44.2 (+1.6 [-1.7, +5.0]) |
| Sindhi | yes / ? / yes | 50 | 47.3 | 36.8 (-10.6 [-14.0, -7.2]) | 55.1 (+7.8 [+4.8, +11.0]) |
| Tamil | yes / ? / yes | 50 | 53.1 | 54.8 (+1.7 [-1.6, +5.0]) | 60.1 (+7.0 [+3.7, +10.5]) |
| Telugu | yes / ? / yes | 50 | 53.9 | 55.1 (+1.2 [-1.9, +4.3]) | 65.3 (+11.5 [+8.3, +14.9]) |
| Urdu | yes / ? / yes | 50 | 57.9 | 60.6 (+2.7 [-0.7, +6.1]) | 71.0 (+13.1 [+10.0, +16.9]) |
| **macro, all (22)** |  | 50 | 52.2 | 47.7 (-4.5 [-7.1, -2.4]) | 62.5 (+10.3 [+8.1, +12.4]) |
| **macro, one script (18)** |  | 50 | 53.6 | 51.5 (-2.1 [-4.4, -0.1]) | 64.3 (+10.7 [+8.2, +13.2]) |

### COMET, mean segment score x 100 (higher is better), English -> X

| language | support | n | sarvam-int4 | gemma-int4@neutral | indictrans2 |
|---|---:|---:|---:|---:|---:|
| Assamese | yes / ? / yes | 50 | 86.3 | 63.5 (-22.9 [-28.7, -18.0]) | 85.0 (-1.4 [-2.4, -0.4]) |
| Bengali | yes / ? / yes | 50 | 88.2 | 84.9 (-3.3 [-5.1, -1.5]) | 87.4 (-0.8 [-2.0, +0.3]) |
| Bodo | yes / ? / yes | 50 | 63.1 | 25.3 (-37.8 [-40.5, -35.0]) | 62.1 (-1.0 [-2.7, +1.0]) |
| Dogri | yes / ? / yes | 50 | 64.7 | 52.2 (-12.6 [-15.9, -9.5]) | 64.2 (-0.6 [-2.3, +1.4]) |
| Konkani | yes / ? / yes | 50 | 58.7 | 51.3 (-7.4 [-10.9, -4.3]) | 58.6 (-0.1 [-1.8, +1.7]) |
| Gujarati | yes / ? / yes | 50 | 89.2 | 86.2 (-3.0 [-4.2, -1.8]) | 89.0 (-0.2 [-0.8, +0.5]) |
| Hindi | yes / ? / yes | 50 | 82.1 | 80.0 (-2.1 [-3.6, -0.4]) | 79.8 (-2.2 [-4.7, -0.4]) |
| Kannada | yes / ? / yes | 50 | 87.1 | 69.6 (-17.5 [-20.9, -14.4]) | 85.6 (-1.5 [-2.6, -0.6]) |
| Kashmiri | yes / ? / yes | 50 | 70.4 | 33.1 (-37.3 [-40.8, -34.0]) | 62.3 (-8.2 [-10.3, -6.0]) |
| Maithili | yes / ? / yes | 50 | 68.5 | 60.7 (-7.8 [-11.6, -4.6]) | 67.8 (-0.7 [-1.9, +0.4]) |
| Malayalam | yes / ? / yes | 50 | 89.1 | 62.2 (-26.9 [-31.6, -22.8]) | 88.4 (-0.6 [-1.4, +0.1]) |
| Marathi | yes / ? / yes | 50 | 78.3 | 73.3 (-5.0 [-7.2, -3.0]) | 76.8 (-1.5 [-2.8, +0.1]) |
| Manipuri | yes / ? / yes | 50 | 88.7 | 58.3 (-30.3 [-37.0, -24.1]) | 84.9 (-3.8 [-6.0, -1.8]) |
| Nepali | yes / ? / yes | 50 | 82.6 | 76.1 (-6.5 [-9.7, -2.9]) | 82.8 (+0.2 [-2.0, +2.9]) |
| Odia | yes / ? / yes | 50 | 86.1 | 54.5 (-31.6 [-35.6, -27.7]) | 80.3 (-5.8 [-7.1, -4.5]) |
| Punjabi | yes / ? / yes | 50 | 83.0 | 72.6 (-10.3 [-12.3, -8.3]) | 82.3 (-0.7 [-1.7, +0.2]) |
| Sanskrit | yes / ? / yes | 50 | 78.6 | 55.6 (-23.0 [-25.4, -20.5]) | 76.4 (-2.3 [-4.7, -0.1]) |
| Santali | yes / ? / yes | 50 | 88.7 | 17.4 (-71.3 [-72.5, -70.0]) | 84.8 (-3.9 [-6.0, -2.1]) |
| Sindhi | yes / ? / yes | 50 | 59.2 | 37.9 (-21.3 [-24.5, -18.3]) | 56.2 (-3.1 [-5.3, -0.8]) |
| Tamil | yes / ? / yes | 50 | 90.4 | 87.5 (-2.8 [-5.5, -0.8]) | 88.5 (-1.8 [-3.1, -0.7]) |
| Telugu | yes / ? / yes | 50 | 87.6 | 85.4 (-2.2 [-3.4, -1.1]) | 87.3 (-0.3 [-1.2, +0.5]) |
| Urdu | yes / ? / yes | 50 | 87.5 | 76.6 (-10.9 [-13.5, -8.3]) | 86.7 (-0.8 [-1.7, +0.2]) |
| **macro, all (22)** |  | 50 | 79.9 | 62.0 (-17.9 [-18.8, -17.1]) | 78.0 (-1.9 [-2.4, -1.3]) |
| **macro, one script (18)** |  | 50 | 80.6 | 67.6 (-13.0 [-13.9, -12.1]) | 79.4 (-1.2 [-1.7, -0.8]) |
| **macro, XLM-R's languages (14)** |  | 50 | 85.4 | 73.4 (-12.0 [-13.0, -11.0]) | 84.0 (-1.4 [-2.0, -0.9]) |

### COMET, mean segment score x 100 (higher is better), X -> English

| language | support | n | sarvam-int4 | gemma-int4@neutral | indictrans2 |
|---|---:|---:|---:|---:|---:|
| Assamese | yes / ? / yes | 50 | 84.4 | 84.7 (+0.3 [-1.6, +2.3]) | 88.0 (+3.6 [+1.6, +5.7]) |
| Bengali | yes / ? / yes | 50 | 86.5 | 87.8 (+1.3 [+0.1, +2.5]) | 89.1 (+2.6 [+1.1, +3.9]) |
| Bodo | yes / ? / yes | 50 | 76.9 | 56.3 (-20.6 [-23.8, -17.5]) | 80.6 (+3.7 [+1.7, +5.9]) |
| Dogri | yes / ? / yes | 50 | 82.0 | 72.7 (-9.3 [-13.1, -5.8]) | 86.4 (+4.4 [+2.8, +5.9]) |
| Konkani | yes / ? / yes | 50 | 79.4 | 74.5 (-4.9 [-7.5, -2.6]) | 81.7 (+2.4 [+0.4, +4.6]) |
| Gujarati | yes / ? / yes | 50 | 87.7 | 88.1 (+0.4 [-0.8, +1.8]) | 90.2 (+2.5 [+1.2, +4.1]) |
| Hindi | yes / ? / yes | 50 | 87.1 | 87.6 (+0.5 [-0.8, +1.9]) | 89.0 (+1.8 [+0.8, +3.0]) |
| Kannada | yes / ? / yes | 50 | 85.3 | 85.0 (-0.3 [-2.2, +1.4]) | 88.4 (+3.0 [+1.4, +4.6]) |
| Kashmiri | yes / ? / yes | 50 | 77.3 | 62.9 (-14.5 [-17.7, -10.8]) | 79.4 (+2.1 [+0.2, +4.3]) |
| Maithili | yes / ? / yes | 50 | 83.8 | 81.1 (-2.7 [-4.1, -1.1]) | 86.2 (+2.3 [+0.7, +3.9]) |
| Malayalam | yes / ? / yes | 50 | 86.7 | 86.9 (+0.1 [-0.8, +1.2]) | 89.1 (+2.4 [+0.8, +3.9]) |
| Marathi | yes / ? / yes | 50 | 85.8 | 86.9 (+1.0 [-0.0, +2.1]) | 88.6 (+2.8 [+1.7, +3.9]) |
| Manipuri | yes / ? / yes | 50 | 74.5 | 43.7 (-30.8 [-33.4, -28.3]) | 76.5 (+2.0 [-0.5, +4.1]) |
| Nepali | yes / ? / yes | 50 | 89.3 | 88.9 (-0.4 [-1.5, +0.7]) | 91.5 (+2.2 [+1.5, +2.9]) |
| Odia | yes / ? / yes | 50 | 87.3 | 82.6 (-4.7 [-7.0, -2.6]) | 88.9 (+1.6 [+0.2, +3.0]) |
| Punjabi | yes / ? / yes | 50 | 84.2 | 84.8 (+0.6 [-1.0, +2.3]) | 87.2 (+3.0 [+1.7, +4.4]) |
| Sanskrit | yes / ? / yes | 50 | 83.5 | 77.1 (-6.4 [-8.6, -4.3]) | 84.5 (+1.1 [-0.6, +2.8]) |
| Santali | yes / ? / yes | 50 | 67.9 | 54.6 (-13.3 [-16.2, -10.3]) | 65.3 (-2.5 [-5.4, +0.2]) |
| Sindhi | yes / ? / yes | 50 | 78.5 | 64.2 (-14.2 [-18.2, -10.5]) | 80.4 (+1.9 [+0.1, +4.2]) |
| Tamil | yes / ? / yes | 50 | 86.2 | 87.1 (+1.0 [-0.2, +2.3]) | 88.5 (+2.4 [+1.3, +3.7]) |
| Telugu | yes / ? / yes | 50 | 87.2 | 86.7 (-0.5 [-1.5, +0.6]) | 89.4 (+2.2 [+1.3, +3.1]) |
| Urdu | yes / ? / yes | 50 | 87.0 | 87.2 (+0.2 [-1.1, +1.4]) | 89.8 (+2.8 [+1.8, +3.9]) |
| **macro, all (22)** |  | 50 | 83.1 | 77.8 (-5.3 [-6.2, -4.5]) | 85.4 (+2.3 [+1.5, +3.1]) |
| **macro, one script (18)** |  | 50 | 85.0 | 82.6 (-2.5 [-3.2, -1.7]) | 87.6 (+2.6 [+1.7, +3.4]) |
| **macro, XLM-R's languages (14)** |  | 50 | 86.3 | 85.8 (-0.5 [-1.2, +0.2]) | 88.7 (+2.4 [+1.7, +3.1]) |

### bits per reference character (lower is better), English -> X

| language | support | n | sarvam-int4 | sarvam-int8 | gemma-int4@neutral |
|---|---:|---:|---:|---:|---:|
| Assamese | yes / ? / yes | 50 | 0.619 | 0.613 (-0.006 [-0.009, -0.003]) | 3.123 (+2.504 [+2.350, +2.664]) |
| Bengali | yes / ? / yes | 50 | 0.501 | 0.499 (-0.002 [-0.004, +0.001]) | 1.584 (+1.084 [+0.988, +1.186]) |
| Bodo | yes / ? / yes | 50 | 0.631 | 0.626 (-0.005 [-0.009, -0.001]) | 4.149 (+3.518 [+3.326, +3.723]) |
| Dogri | yes / ? / yes | 50 | 0.453 | 0.449 (-0.003 [-0.007, +0.001]) | 3.018 (+2.566 [+2.383, +2.782]) |
| Konkani | yes / ? / yes | 50 | 0.725 | 0.718 (-0.007 [-0.011, -0.003]) | 3.930 (+3.205 [+2.939, +3.520]) |
| Gujarati | yes / ? / yes | 50 | 0.541 | 0.541 (-0.001 [-0.003, +0.002]) | 1.777 (+1.235 [+1.091, +1.395]) |
| Hindi | yes / ? / yes | 50 | 0.448 | 0.444 (-0.004 [-0.006, -0.002]) | 1.181 (+0.733 [+0.652, +0.828]) |
| Kannada | yes / ? / yes | 50 | 0.468 | 0.465 (-0.003 [-0.005, -0.001]) | 2.340 (+1.872 [+1.746, +1.996]) |
| Kashmiri | yes / ? / yes | 50 | 1.026 | 1.014 (-0.012 [-0.015, -0.007]) | 4.891 (+3.866 [+3.627, +4.134]) |
| Maithili | yes / ? / yes | 50 | 0.648 | 0.645 (-0.002 [-0.005, +0.000]) | 2.724 (+2.076 [+1.862, +2.321]) |
| Malayalam | yes / ? / yes | 50 | 0.461 | 0.459 (-0.002 [-0.004, +0.000]) | 2.186 (+1.725 [+1.557, +1.893]) |
| Marathi | yes / ? / yes | 50 | 0.441 | 0.439 (-0.001 [-0.003, +0.001]) | 1.469 (+1.028 [+0.921, +1.142]) |
| Manipuri | yes / ? / yes | 50 | 0.744 | 0.740 (-0.004 [-0.009, +0.000]) | 5.850 (+5.106 [+4.849, +5.398]) |
| Nepali | yes / ? / yes | 50 | 0.542 | 0.540 (-0.002 [-0.005, +0.001]) | 2.102 (+1.560 [+1.420, +1.702]) |
| Odia | yes / ? / yes | 50 | 0.517 | 0.512 (-0.006 [-0.008, -0.003]) | 3.537 (+3.020 [+2.836, +3.202]) |
| Punjabi | yes / ? / yes | 50 | 0.938 | 0.937 (-0.000 [-0.004, +0.003]) | 3.033 (+2.096 [+1.898, +2.300]) |
| Sanskrit | yes / ? / yes | 50 | 0.835 | 0.824 (-0.010 [-0.014, -0.006]) | 3.387 (+2.552 [+2.393, +2.740]) |
| Santali | yes / ? / yes | 50 | 1.081 | 1.071 (-0.010 [-0.014, -0.005]) | 4.887 (+3.807 [+3.642, +3.974]) |
| Sindhi | yes / ? / yes | 50 | 1.032 | 1.022 (-0.010 [-0.014, -0.005]) | 4.718 (+3.686 [+3.318, +4.105]) |
| Tamil | yes / ? / yes | 50 | 0.444 | 0.442 (-0.002 [-0.004, -0.000]) | 1.188 (+0.744 [+0.675, +0.827]) |
| Telugu | yes / ? / yes | 50 | 0.540 | 0.538 (-0.002 [-0.005, +0.000]) | 1.668 (+1.127 [+0.987, +1.266]) |
| Urdu | yes / ? / yes | 50 | 0.358 | 0.355 (-0.002 [-0.004, -0.000]) | 1.421 (+1.063 [+0.944, +1.183]) |
| **macro, all (22)** |  | 50 | 0.636 | 0.632 (-0.004 [-0.005, -0.004]) | 2.917 (+2.281 [+2.186, +2.393]) |
| **macro, one script (18)** |  | 50 | 0.561 | 0.558 (-0.003 [-0.004, -0.003]) | 2.434 (+1.873 [+1.792, +1.962]) |

### bits per reference character (lower is better), X -> English

| language | support | n | sarvam-int4 | sarvam-int8 | gemma-int4@neutral |
|---|---:|---:|---:|---:|---:|
| Assamese | yes / ? / yes | 50 | 0.497 | 0.493 (-0.004 [-0.013, +0.005]) | 1.387 (+0.890 [+0.754, +1.037]) |
| Bengali | yes / ? / yes | 50 | 0.502 | 0.493 (-0.009 [-0.019, +0.001]) | 1.100 (+0.598 [+0.506, +0.688]) |
| Bodo | yes / ? / yes | 50 | 0.555 | 0.549 (-0.006 [-0.015, +0.002]) | 1.601 (+1.046 [+0.929, +1.166]) |
| Dogri | yes / ? / yes | 50 | 0.456 | 0.451 (-0.005 [-0.014, +0.004]) | 1.313 (+0.857 [+0.749, +0.978]) |
| Konkani | yes / ? / yes | 50 | 0.605 | 0.603 (-0.002 [-0.013, +0.008]) | 1.528 (+0.923 [+0.819, +1.032]) |
| Gujarati | yes / ? / yes | 50 | 0.502 | 0.500 (-0.003 [-0.013, +0.009]) | 1.087 (+0.584 [+0.482, +0.694]) |
| Hindi | yes / ? / yes | 50 | 0.528 | 0.519 (-0.009 [-0.019, +0.001]) | 1.188 (+0.660 [+0.562, +0.773]) |
| Kannada | yes / ? / yes | 50 | 0.490 | 0.484 (-0.006 [-0.013, +0.003]) | 1.188 (+0.698 [+0.601, +0.806]) |
| Kashmiri | yes / ? / yes | 50 | 0.587 | 0.589 (+0.002 [-0.008, +0.010]) | 1.557 (+0.970 [+0.859, +1.106]) |
| Maithili | yes / ? / yes | 50 | 0.501 | 0.501 (+0.000 [-0.009, +0.010]) | 1.292 (+0.790 [+0.664, +0.938]) |
| Malayalam | yes / ? / yes | 50 | 0.507 | 0.508 (+0.001 [-0.009, +0.011]) | 1.317 (+0.810 [+0.695, +0.911]) |
| Marathi | yes / ? / yes | 50 | 0.509 | 0.509 (-0.000 [-0.009, +0.009]) | 1.190 (+0.681 [+0.593, +0.771]) |
| Manipuri | yes / ? / yes | 50 | 0.541 | 0.536 (-0.005 [-0.011, +0.001]) | 1.872 (+1.331 [+1.199, +1.477]) |
| Nepali | yes / ? / yes | 50 | 0.464 | 0.463 (-0.001 [-0.011, +0.009]) | 1.104 (+0.640 [+0.545, +0.735]) |
| Odia | yes / ? / yes | 50 | 0.471 | 0.466 (-0.005 [-0.012, +0.001]) | 1.324 (+0.852 [+0.742, +0.959]) |
| Punjabi | yes / ? / yes | 50 | 0.588 | 0.582 (-0.006 [-0.015, +0.004]) | 1.374 (+0.787 [+0.672, +0.893]) |
| Sanskrit | yes / ? / yes | 50 | 0.605 | 0.604 (-0.002 [-0.010, +0.006]) | 1.611 (+1.005 [+0.903, +1.124]) |
| Santali | yes / ? / yes | 50 | 0.611 | 0.609 (-0.002 [-0.009, +0.004]) | 1.590 (+0.979 [+0.874, +1.090]) |
| Sindhi | yes / ? / yes | 50 | 0.571 | 0.571 (-0.000 [-0.008, +0.009]) | 1.461 (+0.890 [+0.777, +1.002]) |
| Tamil | yes / ? / yes | 50 | 0.551 | 0.550 (-0.001 [-0.009, +0.007]) | 1.311 (+0.760 [+0.650, +0.864]) |
| Telugu | yes / ? / yes | 50 | 0.529 | 0.528 (-0.001 [-0.009, +0.008]) | 1.168 (+0.639 [+0.535, +0.745]) |
| Urdu | yes / ? / yes | 50 | 0.464 | 0.465 (+0.000 [-0.009, +0.010]) | 0.974 (+0.510 [+0.425, +0.592]) |
| **macro, all (22)** |  | 50 | 0.529 | 0.526 (-0.003 [-0.009, +0.003]) | 1.343 (+0.814 [+0.742, +0.891]) |
| **macro, one script (18)** |  | 50 | 0.518 | 0.515 (-0.003 [-0.010, +0.003]) | 1.281 (+0.763 [+0.689, +0.838]) |

### bits per reference character with the end-of-answer token (lower is better), English -> X

| language | support | n | sarvam-int4 | sarvam-int8 | gemma-int4@neutral |
|---|---:|---:|---:|---:|---:|
| Assamese | yes / ? / yes | 50 | 0.619 | 0.613 (-0.006 [-0.009, -0.003]) | 3.123 (+2.504 [+2.350, +2.664]) |
| Bengali | yes / ? / yes | 50 | 0.501 | 0.499 (-0.002 [-0.004, +0.001]) | 1.584 (+1.084 [+0.988, +1.186]) |
| Bodo | yes / ? / yes | 50 | 0.631 | 0.626 (-0.005 [-0.009, -0.001]) | 4.149 (+3.518 [+3.326, +3.723]) |
| Dogri | yes / ? / yes | 50 | 0.453 | 0.449 (-0.003 [-0.007, +0.001]) | 3.018 (+2.566 [+2.383, +2.782]) |
| Konkani | yes / ? / yes | 50 | 0.725 | 0.718 (-0.007 [-0.011, -0.003]) | 3.933 (+3.208 [+2.939, +3.525]) |
| Gujarati | yes / ? / yes | 50 | 0.542 | 0.542 (-0.001 [-0.003, +0.002]) | 1.780 (+1.238 [+1.092, +1.396]) |
| Hindi | yes / ? / yes | 50 | 0.448 | 0.444 (-0.004 [-0.006, -0.002]) | 1.181 (+0.733 [+0.653, +0.828]) |
| Kannada | yes / ? / yes | 50 | 0.468 | 0.465 (-0.003 [-0.005, -0.001]) | 2.347 (+1.878 [+1.753, +2.010]) |
| Kashmiri | yes / ? / yes | 50 | 1.026 | 1.014 (-0.012 [-0.015, -0.007]) | 4.893 (+3.867 [+3.628, +4.136]) |
| Maithili | yes / ? / yes | 50 | 0.648 | 0.645 (-0.002 [-0.005, +0.000]) | 2.724 (+2.077 [+1.862, +2.321]) |
| Malayalam | yes / ? / yes | 50 | 0.461 | 0.459 (-0.002 [-0.004, +0.000]) | 2.188 (+1.727 [+1.558, +1.895]) |
| Marathi | yes / ? / yes | 50 | 0.441 | 0.439 (-0.001 [-0.003, +0.001]) | 1.469 (+1.029 [+0.922, +1.142]) |
| Manipuri | yes / ? / yes | 50 | 0.744 | 0.740 (-0.004 [-0.009, +0.000]) | 5.860 (+5.116 [+4.858, +5.408]) |
| Nepali | yes / ? / yes | 50 | 0.542 | 0.540 (-0.002 [-0.005, +0.001]) | 2.102 (+1.561 [+1.421, +1.703]) |
| Odia | yes / ? / yes | 50 | 0.517 | 0.512 (-0.006 [-0.008, -0.003]) | 3.539 (+3.022 [+2.839, +3.204]) |
| Punjabi | yes / ? / yes | 50 | 0.938 | 0.937 (-0.000 [-0.004, +0.003]) | 3.035 (+2.097 [+1.899, +2.301]) |
| Sanskrit | yes / ? / yes | 50 | 0.835 | 0.824 (-0.010 [-0.014, -0.006]) | 3.390 (+2.555 [+2.395, +2.743]) |
| Santali | yes / ? / yes | 50 | 1.081 | 1.071 (-0.010 [-0.014, -0.005]) | 4.889 (+3.809 [+3.643, +3.976]) |
| Sindhi | yes / ? / yes | 50 | 1.032 | 1.022 (-0.010 [-0.014, -0.005]) | 4.720 (+3.688 [+3.320, +4.107]) |
| Tamil | yes / ? / yes | 50 | 0.444 | 0.442 (-0.002 [-0.004, -0.000]) | 1.188 (+0.745 [+0.675, +0.827]) |
| Telugu | yes / ? / yes | 50 | 0.540 | 0.538 (-0.002 [-0.005, +0.000]) | 1.668 (+1.128 [+0.987, +1.266]) |
| Urdu | yes / ? / yes | 50 | 0.360 | 0.358 (-0.002 [-0.004, -0.001]) | 1.421 (+1.061 [+0.940, +1.180]) |
| **macro, all (22)** |  | 50 | 0.636 | 0.632 (-0.004 [-0.005, -0.004]) | 2.918 (+2.282 [+2.188, +2.395]) |
| **macro, one script (18)** |  | 50 | 0.562 | 0.558 (-0.003 [-0.004, -0.003]) | 2.436 (+1.874 [+1.793, +1.963]) |

### bits per reference character with the end-of-answer token (lower is better), X -> English

| language | support | n | sarvam-int4 | sarvam-int8 | gemma-int4@neutral |
|---|---:|---:|---:|---:|---:|
| Assamese | yes / ? / yes | 50 | 0.497 | 0.493 (-0.004 [-0.013, +0.005]) | 1.387 (+0.890 [+0.754, +1.037]) |
| Bengali | yes / ? / yes | 50 | 0.502 | 0.493 (-0.009 [-0.019, +0.001]) | 1.100 (+0.598 [+0.506, +0.688]) |
| Bodo | yes / ? / yes | 50 | 0.555 | 0.549 (-0.006 [-0.015, +0.002]) | 1.607 (+1.052 [+0.937, +1.175]) |
| Dogri | yes / ? / yes | 50 | 0.456 | 0.451 (-0.005 [-0.014, +0.004]) | 1.317 (+0.861 [+0.752, +0.985]) |
| Konkani | yes / ? / yes | 50 | 0.605 | 0.603 (-0.002 [-0.013, +0.008]) | 1.531 (+0.926 [+0.822, +1.035]) |
| Gujarati | yes / ? / yes | 50 | 0.502 | 0.500 (-0.003 [-0.013, +0.009]) | 1.087 (+0.584 [+0.482, +0.694]) |
| Hindi | yes / ? / yes | 50 | 0.528 | 0.519 (-0.009 [-0.019, +0.001]) | 1.188 (+0.660 [+0.562, +0.773]) |
| Kannada | yes / ? / yes | 50 | 0.490 | 0.484 (-0.006 [-0.013, +0.003]) | 1.188 (+0.698 [+0.601, +0.806]) |
| Kashmiri | yes / ? / yes | 50 | 0.587 | 0.589 (+0.002 [-0.008, +0.010]) | 1.562 (+0.975 [+0.861, +1.111]) |
| Maithili | yes / ? / yes | 50 | 0.501 | 0.501 (+0.000 [-0.009, +0.010]) | 1.292 (+0.790 [+0.665, +0.938]) |
| Malayalam | yes / ? / yes | 50 | 0.507 | 0.508 (+0.001 [-0.009, +0.011]) | 1.317 (+0.810 [+0.694, +0.911]) |
| Marathi | yes / ? / yes | 50 | 0.509 | 0.509 (-0.000 [-0.009, +0.009]) | 1.190 (+0.681 [+0.593, +0.771]) |
| Manipuri | yes / ? / yes | 50 | 0.541 | 0.536 (-0.005 [-0.011, +0.001]) | 1.912 (+1.371 [+1.241, +1.512]) |
| Nepali | yes / ? / yes | 50 | 0.464 | 0.463 (-0.001 [-0.011, +0.009]) | 1.104 (+0.640 [+0.545, +0.735]) |
| Odia | yes / ? / yes | 50 | 0.471 | 0.466 (-0.005 [-0.013, +0.001]) | 1.324 (+0.852 [+0.742, +0.959]) |
| Punjabi | yes / ? / yes | 50 | 0.588 | 0.582 (-0.006 [-0.015, +0.004]) | 1.374 (+0.787 [+0.672, +0.893]) |
| Sanskrit | yes / ? / yes | 50 | 0.605 | 0.604 (-0.002 [-0.010, +0.006]) | 1.611 (+1.005 [+0.903, +1.124]) |
| Santali | yes / ? / yes | 50 | 0.611 | 0.609 (-0.002 [-0.009, +0.004]) | 1.598 (+0.986 [+0.882, +1.094]) |
| Sindhi | yes / ? / yes | 50 | 0.571 | 0.571 (-0.000 [-0.008, +0.009]) | 1.479 (+0.907 [+0.793, +1.022]) |
| Tamil | yes / ? / yes | 50 | 0.551 | 0.550 (-0.001 [-0.009, +0.007]) | 1.311 (+0.760 [+0.650, +0.864]) |
| Telugu | yes / ? / yes | 50 | 0.529 | 0.528 (-0.001 [-0.009, +0.008]) | 1.168 (+0.639 [+0.535, +0.745]) |
| Urdu | yes / ? / yes | 50 | 0.464 | 0.465 (+0.000 [-0.009, +0.010]) | 0.974 (+0.510 [+0.425, +0.592]) |
| **macro, all (22)** |  | 50 | 0.529 | 0.526 (-0.003 [-0.009, +0.003]) | 1.346 (+0.817 [+0.746, +0.896]) |
| **macro, one script (18)** |  | 50 | 0.518 | 0.515 (-0.003 [-0.010, +0.003]) | 1.282 (+0.764 [+0.689, +0.838]) |

### bits per character of IndicProcessor's pre-processed reference, NOT comparable with the bits above: another text (normalised, tokenised, most Indic scripts transliterated to Devanagari), over the reference's own characters; its end token not counted, English -> X

| language | support | n | indictrans2 |
|---|---:|---:|---:|
| Assamese | yes / ? / yes | 50 | 0.770 |
| Bengali | yes / ? / yes | 50 | 0.575 |
| Bodo | yes / ? / yes | 50 | 0.782 |
| Dogri | yes / ? / yes | 50 | 0.589 |
| Konkani | yes / ? / yes | 50 | 0.905 |
| Gujarati | yes / ? / yes | 50 | 0.610 |
| Hindi | yes / ? / yes | 50 | 0.537 |
| Kannada | yes / ? / yes | 50 | 0.546 |
| Kashmiri | yes / ? / yes | 50 | 1.192 |
| Maithili | yes / ? / yes | 50 | 0.728 |
| Malayalam | yes / ? / yes | 50 | 0.529 |
| Marathi | yes / ? / yes | 50 | 0.515 |
| Manipuri | yes / ? / yes | 50 | 0.981 |
| Nepali | yes / ? / yes | 50 | 0.637 |
| Odia | yes / ? / yes | 50 | 0.595 |
| Punjabi | yes / ? / yes | 50 | 1.005 |
| Sanskrit | yes / ? / yes | 50 | 1.060 |
| Santali | yes / ? / yes | 50 | 1.682 |
| Sindhi | yes / ? / yes | 50 | 1.351 |
| Tamil | yes / ? / yes | 50 | 0.553 |
| Telugu | yes / ? / yes | 50 | 0.620 |
| Urdu | yes / ? / yes | 50 | 0.413 |
| **macro, all (22)** |  | 50 | 0.781 |
| **macro, one script (18)** |  | 50 | 0.665 |

### bits per character of IndicProcessor's pre-processed reference, NOT comparable with the bits above: another text (normalised, tokenised, most Indic scripts transliterated to Devanagari), over the reference's own characters; its end token not counted, X -> English

| language | support | n | indictrans2 |
|---|---:|---:|---:|
| Assamese | yes / ? / yes | 50 | 0.293 |
| Bengali | yes / ? / yes | 50 | 0.292 |
| Bodo | yes / ? / yes | 50 | 0.309 |
| Dogri | yes / ? / yes | 50 | 0.217 |
| Konkani | yes / ? / yes | 50 | 0.364 |
| Gujarati | yes / ? / yes | 50 | 0.292 |
| Hindi | yes / ? / yes | 50 | 0.352 |
| Kannada | yes / ? / yes | 50 | 0.284 |
| Kashmiri | yes / ? / yes | 50 | 0.393 |
| Maithili | yes / ? / yes | 50 | 0.308 |
| Malayalam | yes / ? / yes | 50 | 0.313 |
| Marathi | yes / ? / yes | 50 | 0.294 |
| Manipuri | yes / ? / yes | 50 | 0.346 |
| Nepali | yes / ? / yes | 50 | 0.263 |
| Odia | yes / ? / yes | 50 | 0.260 |
| Punjabi | yes / ? / yes | 50 | 0.415 |
| Sanskrit | yes / ? / yes | 50 | 0.411 |
| Santali | yes / ? / yes | 50 | 0.542 |
| Sindhi | yes / ? / yes | 50 | 0.402 |
| Tamil | yes / ? / yes | 50 | 0.364 |
| Telugu | yes / ? / yes | 50 | 0.322 |
| Urdu | yes / ? / yes | 50 | 0.253 |
| **macro, all (22)** |  | 50 | 0.331 |
| **macro, one script (18)** |  | 50 | 0.311 |

### Tokens per character (the scored references, no BOS; IndicTrans2: of its pre-processed reference, per character of the reference)

| language | characters per sentence | sarvam-translate | gemma-3-4b-it | indictrans2 |
|---|---:|---:|---:|---:|
| English | 155 | 0.214 | 0.214 | 0.221 |
| Assamese | 153 | 0.411 | 0.411 | 0.366 |
| Bengali | 143 | 0.280 | 0.280 | 0.251 |
| Bodo | 160 | 0.457 | 0.457 | 0.254 |
| Dogri | 151 | 0.374 | 0.374 | 0.268 |
| Konkani | 145 | 0.410 | 0.410 | 0.286 |
| Gujarati | 142 | 0.433 | 0.433 | 0.261 |
| Hindi | 156 | 0.281 | 0.281 | 0.250 |
| Kannada | 163 | 0.408 | 0.408 | 0.248 |
| Kashmiri | 157 | 0.570 | 0.570 | 0.293 |
| Maithili | 146 | 0.347 | 0.347 | 0.249 |
| Malayalam | 176 | 0.363 | 0.363 | 0.270 |
| Marathi | 153 | 0.302 | 0.302 | 0.242 |
| Manipuri | 149 | 1.830 | 1.830 | 0.334 |
| Nepali | 148 | 0.325 | 0.325 | 0.236 |
| Odia | 167 | 0.730 | 0.730 | 0.250 |
| Punjabi | 140 | 0.569 | 0.569 | 0.338 |
| Sanskrit | 150 | 0.408 | 0.408 | 0.298 |
| Santali | 162 | 1.016 | 1.016 | 0.284 |
| Sindhi | 152 | 0.432 | 0.432 | 0.291 |
| Tamil | 183 | 0.282 | 0.282 | 0.231 |
| Telugu | 152 | 0.390 | 0.390 | 0.250 |
| Urdu | 148 | 0.335 | 0.335 | 0.276 |

### Speed and memory (generation: greedy)

Not a like-for-like race: engine configs run this repo's sibling engine (Metal INT8/INT4 kernels, continuous batching: a closed loop of `batch` requests in flight); IndicTrans2 runs eager PyTorch through transformers' remote code (static batches of `batch` sources sorted by length, finished rows padded until the batch ends, the encoder run once per batch). Tokens are each model's own (tokens per character below differ), so compare output characters per second. TTFT: from a request's arrival in the engine's queue; for IndicTrans2, from its batch's start (tokenising and the encoder included). One run on one M2 MacBook Air (8 GB), nothing else on the GPU.

| config | stack | weights (GB) | output tok/s | output chars/s | TTFT p50 / p90 (s) | peak GPU (GiB) | peak footprint (GiB) | requests | preempted |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sarvam-int4 | metal-int4 | 2.99 | 21.0 | 59 | 1.02 / 1.83 | 4.52 | 5.57 | 2136 | 1 |
| gemma-int4@neutral | metal-int4 | 2.85 | 27.5 | 75 | 0.86 / 2.03 | 3.75 | 5.78 | 2200 | 153 |
| indictrans2 | hf mps float16 | 2.05 | 115.0 | 514 | 0.35 / 3.98 | 2.26 | 4.32 | 260 | 0 |

### Per-output diagnostics (the directions with any)

| config | direction | outputs | under 50% in the target's script (letters) | stopped by max_new_tokens | with special tokens (removed before scoring) | with other added tokens (kept) |
|---|---:|---:|---:|---:|---:|---:|
| sarvam-int4 | asm-eng | 50 | 0 | 1 | 0 | 0 |
| sarvam-int4 | eng-brx | 50 | 0 | 1 | 0 | 0 |
| sarvam-int4 | eng-npi | 50 | 0 | 1 | 0 | 0 |
| sarvam-int4 | eng-sat | 50 | 0 | 2 | 0 | 0 |
| sarvam-int4 | eng-snd | 50 | 1 | 1 | 0 | 0 |
| sarvam-int4 | kas-eng | 50 | 0 | 1 | 0 | 0 |
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

Scored references whose tokens decode to other text: sarvam-int4 0 / 2200, sarvam-int8 0 / 2200, gemma-int4@neutral 0 / 2200, indictrans2 89 / 2200 (IndicTrans2: of its pre-processed reference).
Code versions (git describe of this repo and the engine; SHA-256 of eval_translate.py with engine_run.py and the engine's src/, or with indictrans.py) per config: sarvam-int4 6f1a79b-dirty 445a9d6ffbd7446e, 9eaa6eb-dirty 2c76e3989512f1e0, a9cbe98-dirty 28b60036a2537030; sarvam-int8 a9cbe98-dirty 28b60036a2537030, c0df389-dirty engine 324313a-dirty 626af229de5f2f07; gemma-int4@neutral c0df389-dirty engine 324313a-dirty 626af229de5f2f07; indictrans2 c0df389-dirty b9870acb3fb415a5, c0df389-dirty f6d4f6bc4922a965.
**Warning:** sarvam-int4's results come from 3 code versions.
**Warning:** sarvam-int8's results come from 2 code versions.
**Warning:** indictrans2's results come from 2 code versions.

### Prompts (each through the model's own chat template; renderings in RUNS/CONFIG/meta.json)

- sarvam-int4: `[{"role": "system", "content": "Translate the text below to {Target}."}, {"role": "user", "content": "{text}"}]`
- sarvam-int8: `[{"role": "system", "content": "Translate the text below to {Target}."}, {"role": "user", "content": "{text}"}]`
- gemma-int4@neutral: `[{"role": "user", "content": "Translate the following text from {Source} to {Target}. Reply with the translation only.\n\n{text}"}]`
- indictrans2: none: IndicProcessor's language tags (`eng_Latn mni_Mtei TEXT`)
