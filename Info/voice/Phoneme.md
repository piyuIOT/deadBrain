## Phoneme Groups
Phoneme are smallest individual sounds produced in a language.

The 9 groups used in `phoneme_focus` come from standard articulatory phonetics (see Ladefoged, *A Course in Phonetics*). They classify sounds by how the mouth/throat physically produces them, not by frequency but in general have a frequency range. 
The BCM tier is a separate axis — the acoustic consequence of that mechanism through a 1.5kHz low-pass filter (3Khz ODR output).

| Group                     | CMU codes                                                                  | BCM tier          |
| ------------------------- | -------------------------------------------------------------------------- | ----------------- |
| Vowels                    | `AA` `AE` `AH` `AO` `AW` `AY` `EH` `ER` `EY` `IH` `IY` `OW` `OY` `UH` `UW` | Tier 1 — survives |
| Nasal consonants          | `M` `N` `NG`                                                               | Tier 1 — survives |
| Voiced stops              | `B` `D` `G`                                                                | Tier 1 — survives |
| Unvoiced stops            | `P` `T` `K`                                                                | Tier 2 — partial  |
| Liquids                   | `L` `R`                                                                    | Tier 2 — partial  |
| Glides                    | `W` `Y` `HH`                                                               | Tier 2 — partial  |
| Fricatives (sibilant)     | `S` `Z` `SH` `ZH`                                                          | Tier 3 — degraded |
| Fricatives (non-sibilant) | `F` `V` `TH` `DH`                                                          | Tier 3 — degraded |
| Affricates                | `CH` `JH`                                                                  | Tier 3 — degraded |

CMU uses these exact codes in its pronouncing dictionary. Stress digits (0/1/2) are appended to vowels only — e.g. `AH0` (unstressed) vs `AH1` (primary stress) — and are stripped when counting groups.