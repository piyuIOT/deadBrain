# Phoneme Frequency Analysis

> Analysed **1,170 sentences** (9,151 words) from `stt_corpus.json`  
> CMU dict coverage: **9,151/9,151 words (100.0%)**  
> Total phoneme tokens: **32,379** across **39 unique phonemes**

---

## Group Summary

| Group | Count | % of all phonemes |
|---|---:|---:|
| Vowels | 12,012 | 37.1% |
| Nasal consonants | 3,028 | 9.4% |
| Voiced stops | 2,455 | 7.6% |
| Unvoiced stops | 4,252 | 13.1% |
| Liquids | 3,217 | 9.9% |
| Glides | 1,352 | 4.2% |
| Fricatives (sibilant) | 3,006 | 9.3% |
| Fricatives (non-sibilant) | 2,590 | 8.0% |
| Affricates | 467 | 1.4% |

---

## Vowels
*12,012 tokens — 37.1% of corpus*

| Phoneme | CMU code | Count | % of all |
|---|---|---:|---:|
| `/ʌ/` | `AH` | 3,146 | 9.72% |
| `/ɪ/` | `IH` | 1,556 | 4.81% |
| `/i/` | `IY` | 978 | 3.02% |
| `/ɑ/` | `AA` | 783 | 2.42% |
| `/ɛ/` | `EH` | 783 | 2.42% |
| `/ɜr/` | `ER` | 759 | 2.34% |
| `/æ/` | `AE` | 727 | 2.25% |
| `/ɔ/` | `AO` | 623 | 1.92% |
| `/u/` | `UW` | 614 | 1.9% |
| `/eɪ/` | `EY` | 587 | 1.81% |
| `/aɪ/` | `AY` | 573 | 1.77% |
| `/oʊ/` | `OW` | 454 | 1.4% |
| `/aʊ/` | `AW` | 211 | 0.65% |
| `/ʊ/` | `UH` | 147 | 0.45% |
| `/ɔɪ/` | `OY` | 71 | 0.22% |

## Nasal consonants
*3,028 tokens — 9.4% of corpus*

| Phoneme | CMU code | Count | % of all |
|---|---|---:|---:|
| `/n/` | `N` | 1,921 | 5.93% |
| `/m/` | `M` | 823 | 2.54% |
| `/ŋ/` | `NG` | 284 | 0.88% |

## Voiced stops
*2,455 tokens — 7.6% of corpus*

| Phoneme | CMU code | Count | % of all |
|---|---|---:|---:|
| `/d/` | `D` | 1,412 | 4.36% |
| `/b/` | `B` | 671 | 2.07% |
| `/g/` | `G` | 372 | 1.15% |

## Unvoiced stops
*4,252 tokens — 13.1% of corpus*

| Phoneme | CMU code | Count | % of all |
|---|---|---:|---:|
| `/t/` | `T` | 2,200 | 6.79% |
| `/k/` | `K` | 1,213 | 3.75% |
| `/p/` | `P` | 839 | 2.59% |

## Liquids
*3,217 tokens — 9.9% of corpus*

| Phoneme | CMU code | Count | % of all |
|---|---|---:|---:|
| `/r/` | `R` | 1,720 | 5.31% |
| `/l/` | `L` | 1,497 | 4.62% |

## Glides
*1,352 tokens — 4.2% of corpus*

| Phoneme | CMU code | Count | % of all |
|---|---|---:|---:|
| `/w/` | `W` | 711 | 2.2% |
| `/h/` | `HH` | 400 | 1.24% |
| `/j/` | `Y` | 241 | 0.74% |

## Fricatives (sibilant)
*3,006 tokens — 9.3% of corpus*

| Phoneme | CMU code | Count | % of all |
|---|---|---:|---:|
| `/s/` | `S` | 1,661 | 5.13% |
| `/z/` | `Z` | 1,050 | 3.24% |
| `/ʃ/` | `SH` | 278 | 0.86% |
| `/ʒ/` | `ZH` | 17 | 0.05% |

## Fricatives (non-sibilant)
*2,590 tokens — 8.0% of corpus*

| Phoneme | CMU code | Count | % of all |
|---|---|---:|---:|
| `/ð/` | `DH` | 1,233 | 3.81% |
| `/f/` | `F` | 685 | 2.12% |
| `/v/` | `V` | 497 | 1.53% |
| `/θ/` | `TH` | 175 | 0.54% |

## Affricates
*467 tokens — 1.4% of corpus*

| Phoneme | CMU code | Count | % of all |
|---|---|---:|---:|
| `/dʒ/` | `JH` | 235 | 0.73% |
| `/tʃ/` | `CH` | 232 | 0.72% |

---

## BCM Survivability Summary

| Tier | Groups | % of corpus |
|---|---|---:|
| Tier 1 — Survive well (<500 Hz) | Vowels, Nasal consonants, Voiced stops | 54.0% |
| Tier 2 — Partial (<1,500 Hz) | Unvoiced stops, Liquids, Glides | 27.2% |
| Tier 3 — Degraded / lost (>1,500 Hz) | Fricatives (sibilant), Fricatives (non-sibilant), Affricates | 18.7% |

> [!note]
> Tier 3 phonemes are hardest for a bone conduction mic to capture cleanly.
> A higher Tier 3 % means the model will need more targeted hard-to-learn recordings.