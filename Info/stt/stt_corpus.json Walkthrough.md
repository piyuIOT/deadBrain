## Structure
Six top-level sections, each with a flat array of objects.

```
stt_corpus.json
├── meta
├── phonetic_sentences     [PHO-xxx]
├── domain_specific        [DOM-xxx]
├── intents                [INT-xxx] → utterances [INT-xxx-yyy]
├── alphanumerics          [ALP-xxx]
├── wake_words             [WKW-xxx] → negatives [WKW-xxx-NEG-yyy]
└── hard_to_learn          [HTL-xxx]
```

---
## Sections

### `phonetic_sentences`
1,170 sentences covering broad American English phoneme distribution.

```json
{
  "id": "PHO-001",
  "text": "The birch canoe slid on the smooth planks.",
  "source": "Harvard Sentences H1",
  "phoneme_focus": ["Vowels", "Nasal consonants", "Fricatives (non-sibilant)"]
}
```

**Sources:**
- PHO-001 → PHO-720: [IEEE Harvard Sentences](https://en.wikipedia.org/wiki/Harvard_sentences) (1965), 72 lists × 10 sentences, designed for phonetic balance in audio testing
- PHO-721 → PHO-1170: [TIMIT SX sentences](https://catalog.ldc.upenn.edu/LDC93S1) (1986), 450 sentences designed for per-speaker phoneme coverage

**`phoneme_focus`** is auto-computed. For each sentence, every word is looked up in the CMU Pronouncing Dictionary, phonemes are counted per group, and the top 3 groups by token count are stored.

---
### `domain_specific`
TEMPLE-specific phrases that are likely to appear in real usage but don't fit in natural sentence list.

```json
{ "id": "DOM-001", "text": "Start recording brainflow data." }
```

---
### `intents`
Grouped by intent name. Each intent has multiple phrasings (utterances) so the model sees natural variation.

```json
{
  "id": "INT-001",
  "intent": "start_activity",
  "utterances": [
    { "id": "INT-001-001", "text": "Start a workout session." },
    { "id": "INT-001-002", "text": "Begin tracking my run." }
  ]
}
```

5-8 utterances per intent. More variation = better generalisation.

---
### `alphanumerics`
Digits, letters, and mixed strings. Needed because STT models trained on natural speech struggle with spelled-out characters.

```json
{ "id": "ALP-001", "text": "A1 B2 C3", "type": "mixed" }
```

`type` is `digits`, `letters`, `date`, `time` etc...

---
### `wake_words`
One entry per wake word model. `phrase` is the target; `negatives` are phonetically confusable phrases used to train the rejection boundary.

```json
{
  "id": "WKW-001",
  "phrase": "Hey Temple",
  "negatives": [
    { "id": "WKW-001-NEG-001", "text": "Hey" },
    { "id": "WKW-001-NEG-002", "text": "Temple" },
    { "id": "WKW-001-NEG-003", "text": "Hey Temporal" }
  ]
}
```

Each wake word is a separate model. Current entries: `Hey Temple`, `OK Temple`, `Oye Temple`.

Negatives here are the ones that should not trigger the engine (half wakewords, phonetically similar words, or totally random sentences)

---
### `hard_to_learn`
Sentences that user flag as not properly recognised gets added here with more variations for further training. 

```json
{
  "id": "HTL-001",
  "text": "She sells seashells by the seashore.",
  "reason": "fricative-heavy",
  "phoneme_focus": ["/s/", "/ʃ/"],
  "min_recordings_per_speaker": 10
}
```