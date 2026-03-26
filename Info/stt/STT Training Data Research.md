---
tags: [research, STT, speech, bone-conduction, NLP, machine-learning, data-collection]
created: 2026-03-18
status: complete
---

# STT Training Data Research — Bone Conduction Microphone Edition

> **Context:** Building a crowdsourced speech data collection app for a bone conduction microphone (BCM) capped at ~1,500 Hz. Users open the app, see a text prompt, record themselves speaking it, and stop. Audio + ground truth transcript streamed to backend for STT model training.

---

## The Core Question

> What text do you show users on the recording screen, and why?

The answer has four layers and is driven entirely by two constraints:
1. **Your hardware** — a BCM that only passes audio up to ~1,500 Hz
2. **Your model goal** — accurate transcription (STT) and/or command recognition (intent)

---

## 1. The Bone Conduction Constraint (Read This First)

Your 1,500 Hz ceiling is not just a spec — it determines what phonemes your model can ever learn to distinguish, and therefore what your training text must prioritize.

### What Survives vs What Dies at 1,500 Hz

Standard speech lives in two formant bands:
- **F1** (first formant): 200–1,000 Hz → **fully captured** by your BCM
- **F2** (second formant): 700–2,500 Hz → **only lower half captured**

| Phoneme Group                                              | BCM Status  | Notes                                                       |
| ---------------------------------------------------------- | ----------- | ----------------------------------------------------------- |
| **All vowels** /i/ /ɪ/ /e/ /ɛ/ /æ/ /ɑ/ /o/ /ʊ/ /u/ /ʌ/ /ɜ/ | ✅ GOOD      | F1 fully captured; partial F2 — main discriminant preserved |
| **Nasal consonants** /m/ /n/ /ŋ/                           | ✅ GOOD      | Nasal murmur peaks at 250–500 Hz                            |
| **Voiced stops** /b/ /d/ /g/                               | ✅ GOOD      | Voice bar + burst, voicing cue clear                        |
| **Unvoiced stops** /p/ /t/ /k/                             | ⚠️ MODERATE | Burst present, voiced/unvoiced contrast weaker              |
| **Liquids** /l/ /r/                                        | ⚠️ MODERATE | /l/ has extra formant at ~1,500 Hz — right at your edge     |
| **Glides** /w/ /j/ /h/                                     | ⚠️ MODERATE | Glide transitions up to ~1 kHz                              |
| **Fricatives** /s/ /z/ /ʃ/ /ʒ/                             | ❌ POOR      | Energy at 3–8 kHz — nearly absent                           |
| **Fricatives** /f/ /v/ /θ/ /ð/                             | ❌ POOR      | Energy 1–8 kHz — heavily degraded                           |
| **Affricates** /tʃ/ /dʒ/                                   | ❌ POOR      | Stop portion survives; fricative tail does not              |

### Key Implication

> Your model will learn to infer fricatives from **surrounding vowel context**, not from the fricative signal itself. "She sells sea shells" sounds like mush at 1,500 Hz — but the vowel transitions /iː/ → /ɛ/ → /iː/ → /ɛ/ are perfectly preserved.

**Do NOT exclude fricative-heavy sentences.** Include them — the model needs to learn what degraded fricatives look like. But *over-represent* vowel-nasal-stop-rich sentences because those are your cleanest signal.

---

## 2. The Four-Layer Text Stack

Use this as your prompt bank architecture. Every user sees all four layers across sessions.

### Layer 1 — Phonetically Balanced Sentences (40% of prompts)

**What:** Sentences engineered to cover all English phonemes in natural proportion.
**Source:** Harvard Sentences (IEEE) + TIMIT-style phonetically compact sentences.
**Why:** This is your acoustic backbone. Without it, your model has phoneme blind spots.

**Design rules:**
- 6–14 words per sentence (1.5–4 seconds natural speech)
- Cover all surviving BCM phonemes, especially every vowel contrast
- Use common, familiar words — unfamiliar words cause spell-reading (sounds robotic)
- Include some fricative-heavy sentences even though they degrade (model needs the context pattern)

**Ready-to-use: Harvard Sentences (List 1 — public domain)**
```
"The birch canoe slid on the smooth planks."
"Glue the sheet to the dark blue background."
"It's easy to tell the depth of a well."
"These days a chicken leg is a rare dish."
"Rice is often served in round bowls."
"The juice of lemons makes fine punch."
"The box was thrown beside the parked truck."
"The hogs were fed chopped corn and garbage."
"Four hours of steady work faced us."
"Large size in stockings is hard to sell."
```

All 72 lists (720 sentences) are available from the IEEE and Columbia University speech lab.

**Phoneme coverage priority for BCM (order matters):**
1. All vowel sounds across F1 range
2. Nasal consonants in multiple positions (initial, medial, final)
3. Voiced vs unvoiced stop contrasts (/b/-/p/, /d/-/t/, /g/-/k/)
4. Liquid + glide consonants
5. Fricatives (include even though degraded)

---

### Layer 2 — Domain-Specific Sentences (30% of prompts)

**What:** Sentences drawn from your actual deployment context.
**Source:** You build these — there is no off-the-shelf substitute.
**Why:** A general English model trained on audiobooks will fail on domain jargon, product names, measurements, and workflow vocabulary.

**How to build your Layer 2 corpus:**
1. Extract 200–500 domain terms: product names, locations, procedures, units, acronyms, proper nouns
2. Write 3–5 sentences per term using it in natural grammatical context
3. Include typical communication patterns: commands, confirmations, status updates, error reports, questions
4. Include number-heavy sentences if your use case has quantities, codes, or identifiers

**Example (warehouse/logistics domain):**
```
"Pallet twelve A is ready for dock door seven."
"The manifest shows forty-eight units of item code three-zero-four-nine."
"Transfer the order to bay number six for quality inspection."
"The temperature in cold storage bay three is minus eighteen degrees."
"Forklift two is due for its monthly maintenance check."
```

**Do NOT use:**
- Sentences with uncommon or archaic words the user won't recognize
- Sentences longer than ~15 words (breath management changes; prosody goes artificial)
- Heavy punctuation like nested clauses or em dashes
- ALL CAPS (users tend to shout)
- Abbreviations like "Dr." or "St." — users pronounce them unpredictably

---

### Layer 3 — Command & Intent Utterances (20% of prompts)

**What:** Multiple distinct phrasings of each command/intent you want to recognize.
**Source:** Designed using Fluent Speech Commands + SNIPS methodology.
**Why:** Intent classifiers need paraphrase diversity. A model that only sees "Turn on the lights" will fail when a user says "Switch the lights on."

**The golden rule from Fluent Speech Commands research:** each intent needs **at minimum 5 distinct surface phrasings**. FSC uses 248 phrasings for 31 intents (avg 8 per intent).

**Example intent table:**

| Intent | Phrasings to collect |
|---|---|
| Start recording | "Start recording" / "Begin recording" / "Record this" / "Go ahead and record" / "Let's start" / "Hit record" |
| Stop recording | "Stop recording" / "End recording" / "Done" / "Stop now" / "Finish" / "That's it" |
| Confirm | "Yes" / "Confirmed" / "That's right" / "Correct" / "Go ahead" / "Affirmative" |
| Cancel | "Cancel" / "No" / "Abort" / "Never mind" / "Discard that" / "Stop" |
| Repeat prompt | "Repeat that" / "Say it again" / "Read again" / "One more time" / "What was that?" |

**Collect each phrasing from each speaker at least twice (different sessions).** This creates intra-speaker variation.

**Also include negative examples** — utterances that sound *near* an intent but should not trigger it. These prevent false positives.

---

### Layer 4 — Digits, Alphanumerics, Edge Cases (10% of prompts)

**What:** Number strings, codes, dates, currency, mixed alphanumeric.
**Why:** Digits are massively underrepresented in natural language corpora but heavily used in real workflows. Models consistently fail on numbers without targeted training.

```
"Zero one two three four five six seven eight nine."
"The order number is four seven three dash alpha bravo two."
"March eighteenth, twenty twenty-six."
"Forty-five dollars and thirty cents."
"Flight AC four seven one departs at fourteen thirty."
"The serial number is X-ray romeo niner four two."
```

---

## 3. What Major STT Systems Use — The Research Playbook

### OpenAI Whisper

**Training data:** 680,000 hours of audio scraped from the internet with *weak supervision* — transcripts came from subtitles, YouTube auto-captions, and podcast captions. Not manually verified.

**Key lessons for you:**
- Scale beats curation at huge volume. Whisper uses imperfect transcripts because noise averages out across 680K hours. You cannot match this.
- Whisper v3 trained on 1M hours labeled + 4M hours pseudo-labeled (labeled by an earlier Whisper version).
- **Web text = enormous lexical diversity.** Whisper already knows most words in existence.

> **The smartest move:** Do not train from scratch. Fine-tune Whisper on your BCM recordings. With fine-tuning, **10–50 hours of BCM-matched domain audio** can yield a highly accurate model. Starting from scratch requires 1,000+ hours and a large team.

### LibriSpeech

- **Source:** 1,000 hours of read English speech from LibriVox audiobooks (Project Gutenberg text)
- **Strengths:** Long complex sentences, rich vocabulary, multiple genres
- **Weakness:** All read speech from literary text — stylistically different from conversational speech
- **Use:** The standard ASR benchmark. If you fine-tune Whisper, you can evaluate against LibriSpeech test sets to compare your model to published baselines.

### Mozilla Common Voice

- **Source:** Crowdsourced readings of CC-licensed text — Wikipedia, public domain books, news articles, user-submitted sentences
- **Current size:** 17,000+ validated hours across 100+ languages
- **Text validation rules:** ≥6 words, no special characters, ≤14 seconds when read naturally, from CC sources, requires 2+ community upvotes before inclusion

> **Steal their QC model:** Show each recording to 2–3 other users. 2+ upvotes = validated. 2+ downvotes = rejected. This is exactly the peer validation model you should implement.

### TIMIT (The Gold Standard for Phonetic Coverage)

- **Source:** Engineered text — not sourced from existing documents. Designed specifically to maximize phoneme coverage.
- **Size:** 6,300 sentences from 630 speakers across 8 US dialect regions
- **Composition:**
  - 2 dialect "shibboleth" sentences per speaker (tests regional pronunciation)
  - 8 sentences from 450 **phonetically compact** sentences (MIT-designed for all-phoneme efficiency)
  - Additional from 1,890 **phonetically diverse** sentences (TI-designed for broad coverage)
- **Still the benchmark** for acoustic-phonetic research after 30+ years

> **Steal their design principle:** Use a greedy phoneme coverage algorithm — select sentences that maximize *new* phoneme-context pairs not yet covered. The CMU Pronouncing Dictionary (134K words with phonetic transcriptions) lets you build this yourself.

### VoxPopuli (Meta AI)

- **Source:** European Parliament recordings — spontaneous formal speech, 23 languages
- **Size:** 400K hours unlabeled audio
- **Use:** Pre-training acoustic models for multilingual systems

---

## 4. Intent / Command Engines — Different Data, Different Strategy

Full STT decodes every word. An intent engine maps the whole utterance to one of N known intents + slot values. The text strategy is fundamentally different.

### SNIPS NLU Dataset

**Stats:** 14,484 utterances, 7 intents, ~2,000+ examples per intent
**Intents:** PlayMusic, AddToPlaylist, RateBook, SearchScreeningEvent, BookRestaurant, GetWeather, SearchCreativeWork
**Published accuracy (2024):** 98.88% intent accuracy, 97.07% slot F1

**What made it influential:** paraphrase diversity per intent. Every intent has hundreds of natural variations. Your training data must mirror this.

**Available at:** https://github.com/snipsco/nlu-benchmark

### Fluent Speech Commands (FSC)

**Stats:** 30,043 utterances, 97 speakers, 31 unique intents, 248 phrasings, 16 kHz WAV
**Intent structure:** {action, object, location} triplets e.g. {activate, lights, kitchen}

This is the reference dataset for how many paraphrases you need per intent. **248 phrasings for 31 intents = avg 8 phrasings per intent.** Aim for this.

**Available at:** https://fluent.ai/fluent-speech-commands-a-dataset-for-spoken-language-understanding-research/

### Google Speech Commands v2

**Stats:** 105,000 recordings of 35 short words, ~3,000 per word, 1 second each, 16 kHz
**Core 10:** yes, no, up, down, left, right, on, off, stop, go

If you need wake words or single-word commands — this is your reference. Collect **300+ positives per keyword** from diverse speakers before deploying a spotter.

### ATIS (Airline Travel Information System)

**Stats:** 4,978 training utterances, 18 intent types, includes slot filling
**Slot filling = extracting named entities:** departure city, date, airline name, etc.

If your intents include parameter extraction (not just classification), ATIS teaches you how to structure the annotation schema.

### Amazon MASSIVE

1 million utterances, 51 intents, 18 languages. The most comprehensive modern intent dataset. Useful if you go multilingual.

---

## 5. Data Collection Strategy

### How Much Data Do You Need?

| Approach | Minimum | Notes |
|---|---|---|
| Fine-tune pre-trained model (recommended) | 10–50 hrs, 50+ speakers | Leverage Whisper's 680K hr foundation |
| Train acoustic model from scratch | 500–1,000 hrs, 200+ speakers | BCM adaptation still needs fine-tuning on top |
| Intent classifier only | 200–500 utterances per intent | 5+ phrasings per intent mandatory |
| Keyword spotter / wake word | 300+ positives per keyword | Plus 5× negative samples (similar-sounding words) |

### Speaker Diversity (Most Underestimated Factor)

Never train on fewer than 50 speakers. 100+ speakers across diverse demographics before you expect real-world generalization.

You need diversity across:
- **Age:** 18–70+. Older speakers have different vocal tract resonances.
- **Gender:** balanced male/female/non-binary
- **Accent/dialect:** regional variation changes vowel realizations significantly
- **Speaking rate:** fast, medium, slow — most corpora skew medium
- **Environment:** if your device will be used in noisy environments, collect some data there too

### Per-User Session Design

| Element | Recommendation |
|---|---|
| Session length | 10–15 min max. Beyond 15 min, fatigue causes disfluencies = bad data |
| Prompts per session | 25–40 sentences |
| Warmup | 3 unrecorded warmup prompts at session start |
| Session frequency | Multiple short sessions over days/weeks beats one long session |
| Prompt order | Randomize. Never show same prompt twice in same session |
| Skip option | Always allow. Forced recordings of unfamiliar text produce hesitations |
| Re-record option | Allow. Flag bad takes for human review — don't auto-delete |

### Prompt Display Schedule Across Sessions

| Session | Layer 1 % | Layer 2 % | Layer 3+4 % |
|---|---|---|---|
| Session 1 (first ever) | 70% | 20% | 10% |
| Session 2 | 50% | 30% | 20% |
| Sessions 3–5 | 40% | 35% | 25% |
| Session 6+ | 30% | 40% | 30% |

Front-load Layer 1 because even users who only complete one session contribute phonetic baseline data.

### Metadata to Collect Per Recording

- Speaker ID (anonymous UUID, not PII)
- Session ID, recording timestamp
- Device model + firmware version
- App version, OS platform
- Prompt ID (links recording to ground truth text)
- Recording duration (ms)
- User-reported environment (quiet / light background / noisy — 3-choice self-report)
- Speaker demographics (voluntary): age bracket, native language, primary region
- Quality flags: re-record attempted? Skipped?

### Quality Control Pipeline

**Stage 1 — Automated (runs on upload):**
- Reject recordings < 0.5s or > 30s
- Reject silence (RMS below threshold)
- Reject clipped audio (peak > −1 dBFS)
- Reject low SNR recordings

**Stage 2 — Peer validation (Common Voice model):**
- Show each recording to 2–3 other users
- "Does this sound like the shown text?" — upvote/downvote
- 2+ upvotes = validated; 2+ downvotes = rejected

**Stage 3 — Expert review:**
- Mixed-vote recordings
- Bottom 5% of automatic quality metrics
- Budget for a human annotator from the start

---

## 6. What NOT to Show on Screen

| ❌ Avoid | Why |
|---|---|
| Uncommon / archaic / technical vocabulary | Users spell-read unfamiliar words — sounds robotic |
| Sentences > 15 words | Breath management changes; prosody becomes artificial |
| Heavy punctuation (nested clauses, em dashes, semicolons) | Users pause at punctuation → recording artifacts |
| ALL CAPS sentences | Users tend to shout |
| Abbreviations: Dr., St., Ave. | Users pronounce these inconsistently ("Doctor" vs "Doctor period") |
| Sentences with numbers written as digits (e.g., "record 43 units") | User may say "forty-three" or "four three" — ambiguous. Write numbers as words in read prompts |

---

## 7. Open Datasets You Can Use or Reference

### STT Training Text Sources

| Resource                        | Use                                          | URL                                     |
| ------------------------------- | -------------------------------------------- | --------------------------------------- |
| Harvard Sentences (IEEE)        | Tier 1 prompts — use directly                | cs.columbia.edu/~hgs/audio/harvard.html |
| CMU Pronouncing Dictionary      | Build phonetically balanced custom sentences | speech.cs.cmu.edu/cgi-bin/cmudict       |
| Common Voice Sentence Collector | CC-licensed sentences, peer-reviewed         | commonvoice.mozilla.org                 |
| Project Gutenberg               | Diverse vocabulary extraction                | gutenberg.org                           |
| Wikipedia dumps                 | Domain vocabulary, CC-BY-SA licensed         | dumps.wikimedia.org                     |

### Intent / Command Data

| Dataset | Size | Intents | URL |
|---|---|---|---|
| SNIPS NLU | 14.5K utterances | 7 | github.com/snipsco/nlu-benchmark |
| Fluent Speech Commands | 30K utterances, audio | 31 | fluent.ai/fluent-speech-commands |
| Google Speech Commands v2 | 105K recordings | 35 keywords | via TensorFlow datasets |
| ATIS | 4,978 utterances | 18 | HuggingFace: itslinear/atis_intents |
| Amazon MASSIVE | 1M utterances | 51 | github.com/alexa/massive |

### Benchmarking / Reference

| Dataset | Size | Use |
|---|---|---|
| LibriSpeech | 1,000 hrs | Standard ASR benchmark |
| TIMIT | 6,300 utterances, 630 speakers | Phoneme diagnostic benchmark |
| VoxPopuli | 400K hrs | Multilingual pre-training |

---

## 8. BCM-Specific Warning

> Research on bone conduction STT consistently shows that models trained on air-conduction audio and directly applied to BCM audio perform very poorly — sometimes **50–80% higher Word Error Rate**.

BCM recordings:
- Sound muffled (low-pass filtered)
- Lack high-frequency fricative energy
- Have different spectral envelope characteristics
- May contain bone-transmitted noise from jaw movement or head vibration

**Even 10 hours of matched BCM training data fine-tuned on top of Whisper will dramatically outperform a generic model applied to BCM audio.**

Collect BCM-specific data from day one. Do not assume a general model will transfer.

---

## 9. Implementation Roadmap

### Phase 1 — Corpus Design (Before User Deployment)
- [ ] Select 500 Layer 1 sentences (Harvard + phonetically balanced)
- [ ] Write 300 Layer 2 domain sentences with domain expert input
- [ ] Design 50–100 Layer 3 command utterances (5+ phrasings per intent)
- [ ] Build 50 Layer 4 digit/alphanumeric prompts
- [ ] Review all prompts for readability, length, vocabulary difficulty
- [ ] Set up backend: recording upload, ground truth storage, metadata schema

### Phase 2 — Internal Collection (10–20 speakers, team + early users)
- [ ] Collect internal recordings to validate app + audio pipeline + QC
- [ ] Verify BCM audio quality at target sample rate and bitrate
- [ ] Run pilot fine-tuning of Whisper on BCM data — establish baseline WER
- [ ] Identify systematic errors, adjust Layer 2 corpus to over-represent failure cases

### Phase 3 — Broad Collection (100+ speakers)
- [ ] Deploy to users; use gamification (streaks, leaderboards) for return sessions
- [ ] Run automated QC + peer validation continuously
- [ ] Track per-speaker layer coverage; prompt under-represented speakers
- [ ] Retrain every 2–4 weeks; track WER improvement

### Phase 4 — Ongoing Maintenance
- [ ] Add Layer 2 sentences as domain expands
- [ ] Collect adversarial examples (utterances model gets wrong) → add to prompt pool
- [ ] Expand speaker diversity as user base grows geographically

---

## Quick Reference: Minimum Viable Corpus Checklist

- [ ] 500+ phonetically balanced sentences (Harvard Sentences as base)
- [ ] 300+ domain-specific sentences with your vocabulary
- [ ] 200+ utterances per intent (5+ distinct phrasings each)
- [ ] 50+ digit/alphanumeric prompts
- [ ] 50+ diverse speakers before first training run
- [ ] Metadata: speaker ID, session ID, prompt ID, duration, environment, device version
- [ ] Automated QC: silence detection, clipping detection, SNR threshold
- [ ] Peer validation: 2+ votes per recording before training inclusion

---

## Sources

- [OpenAI Whisper Paper (Radford et al. 2022)](https://cdn.openai.com/papers/whisper.pdf)
- [TIMIT Corpus — LDC](https://catalog.ldc.upenn.edu/LDC93S1)
- [Fluent Speech Commands (Lugosch et al. 2019)](https://fluent.ai/fluent-speech-commands-a-dataset-for-spoken-language-understanding-research/)
- [SNIPS NLU (Coucke et al. 2018)](https://arxiv.org/pdf/1805.10190)
- [Common Voice (Ardila et al. 2020)](https://aclanthology.org/2020.lrec-1.520/)
- [BCM Speech Research — PMUT-based BCM System (MDPI Micromachines 2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12195400/)
- [Fusing Bone-conduction and Air-conduction Sensors for Speech Enhancement](https://pmc.ncbi.nlm.nih.gov/articles/PMC10147322/)
- [Harvard Sentences — Wikipedia](https://en.wikipedia.org/wiki/Harvard_sentences)
- [TIMIT — Wikipedia](https://en.wikipedia.org/wiki/TIMIT)
- [Open Source STT Datasets — Picovoice](https://picovoice.ai/blog/open-source-speech-to-text-datasets/)
- [Methodology for Obtaining High-Quality Speech Corpora (MDPI 2025)](https://www.mdpi.com/2076-3417/15/4/1848)
- [Mozilla Common Voice Spontaneous Speech](https://www.mozillafoundation.org/en/blog/common-voice-spontaneous-speech/)
- [Reliable ASR Models: How Much Speech Data Is Enough?](https://waywithwords.net/resource/reliable-asr-model-training-data/)
