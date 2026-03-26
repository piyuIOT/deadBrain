> [!note] About this document
> A comprehensive research synthesis on frequency components in human voice — normal speech, vowels, consonants, singing — and how bone conduction changes the picture. Includes practical guidance on frequency restriction and STT viability.

---

## The Building Blocks: F0 and Formants

Before diving into specific activities, two concepts underpin everything:

- **Fundamental Frequency (F0)** — the base pitch; how fast the vocal cords vibrate
- **Formants (F1, F2, F3...)** — resonant peaks shaped by the throat, mouth, and nasal cavity that make vowels *sound like vowels*

Almost all speech intelligibility lives in the relationship between these formants.

| Speaker Type | F0 Range |
|---|---|
| Adult men | 85–180 Hz |
| Adult women | 165–255 Hz |
| Children | 250–400 Hz |

---

## Normal Speech: Vowels vs. Consonants

> [!important] Key Insight
> Vowels and consonants live in **completely different frequency territories**. This is the most important thing to understand.

### Vowels

Vowels are voiced, periodic, and low-energy in high frequencies. Their energy sits primarily in **250–2,000 Hz**, dominated by F1 and F2.

| Vowel Example | F1 | F2 |
|---|---|---|
| "ee" | ~300 Hz | ~2,300 Hz |
| "ah" | ~700 Hz | ~1,200 Hz |
| "oo" | ~300 Hz | ~870 Hz |

Above ~2,000–3,000 Hz, vowel energy drops off sharply. (Note: the F2 of vowels such as "ee" extends to ~2,300 Hz, so energy is still significant up to that point — the drop-off is above F2, not at 1 kHz.)

### Consonants

Consonants split into two categories with very different frequency profiles.

**Voiced consonants** (b, d, g, m, n, z, v):
- Energy primarily in **250–4,000 Hz**
- Share territory with vowels
- Relatively easy to capture

**Unvoiced consonants** (f, s, sh, t, p, th, k):
- Energy peaks in **2,000–8,000 Hz** — the danger zone
- "s" has its highest spectral peak at **5,000–6,000 Hz**
- "f" and "th" live similarly high
- Fricatives as a class are broadband noise-like sounds extending well into 8+ kHz

> [!warning]
> The **2,000–4,000 Hz band is the single most critical band for intelligibility**. This is why telephone systems were designed around 300–3,400 Hz. Most phoneme discrimination happens here.

### Formant Reference

| Formant | Approximate Range |
|---|---|
| F1 | 250–1,000 Hz |
| F2 | 800–2,200 Hz |
| F3 | 1,500–3,500 Hz |
| F4 | 2,500–4,500 Hz |

---

## Singing Voice

Singing significantly extends the frequency picture.

### Fundamental Frequency by Voice Type

| Voice Type | F0 Range      |
| ---------- | ------------- |
| Bass       | ~80–330 Hz    |
| Baritone   | ~110–390 Hz   |
| Tenor      | ~130–520 Hz   |
| Alto       | ~196–700 Hz   |
| Soprano    | ~260–1,050 Hz |

Harmonics (integer multiples of F0) extend energy all the way to **8,000–12,000 Hz and beyond**. Research has recorded harmonic energy up to **20 kHz** in trained singers.

### The Singer's Formant

> [!tip] Singer's Formant
> A clustering of F3, F4, and F5 around **2,800–3,400 Hz** (centered near 3,000 Hz). This resonance is **absent in normal speech** and is what allows a trained opera singer to be heard over a full orchestra without amplification.
>
> - Bandwidth: ~250–500 Hz wide
> - Present in: trained classical singers, especially males
> - A secondary resonance peak near **10,000 Hz** has also been identified in trained tenors

### Overtone / Throat Singing

An extreme case where singers isolate individual harmonics. The throat manipulations create resonance peaks as high as **4,000–5,000 Hz** appearing as a prominent whistle above the drone.

---

## Bone Conduction Voice

### Why It Sounds Different: Skull as Low-Pass Filter

Bone conduction (BC) picks up vibrations transmitted through the skull and tissue rather than through air. Skin, fat, muscle, and bone all attenuate high frequencies more than low frequencies as vibration travels through them.

```
Air Conduction:  ████████████████████████  (full spectrum)
Bone Conduction: ██████████░░░░░░░░░░░░░░  (low-pass filtered)
                 0    1k   2k   3k   4k   8k Hz
```

### BC Frequency Zones

| Frequency Range | BC Behaviour |
|---|---|
| 100–1,500 Hz | **Strong and reliable** — F0, voiced harmonics, F1 all pass well |
| 1,500–2,500 Hz | **Attenuation begins** — the transfer function through skull tissue rolls off here |
| 2,000–2,500 Hz | **Most BC mics lose reliability** above this point |
| 4,000+ Hz | **Essentially absent** — standard clinical BC audiometry routinely tests up to 4,000 Hz; some protocols extend to 8,000 Hz but sensitivity is greatly reduced |

> [!warning] Some lower-quality BC microphones may drop off as early as **750–1,000 Hz** *(approximate, cited from secondary sources; not measured in primary research reviewed here)*

### What BC Preserves vs. Loses

**Preserved in BC:**
- Fundamental frequency (F0) — pitch intact
- Voicing information (voiced vs. unvoiced distinction partially retained)
- Vowel structure — F1 and lower F2 are relatively intact
- Prosody and rhythm

**Lost or severely degraded in BC:**
- Unvoiced fricatives: s, f, sh, th — their 4,000–8,000 Hz energy doesn't travel through bone
- The Singer's Formant (2,800–3,400 Hz) — diminished
- Upper consonant distinction in 2,000–4,000 Hz
- Overall voice sounds muffled, "as if heard through a wall"

### BC Across Activities

| Activity | What BC Captures | What's Lost |
|---|---|---|
| Normal speech | Vowels, voiced consonants, prosody | Unvoiced fricatives, consonant detail |
| Singing | Fundamental pitch, rhythm | Singer's Formant, upper harmonics |
| Whispered speech | Almost nothing — whisper has no voiced F0 | Everything; whisper is entirely high-frequency turbulence |

### BC Advantage: Noise Immunity

> [!success] Key Advantage
> In an environment with **68 dB noise**, BC achieves over **5× better signal-to-noise ratio** than an air conduction microphone. The body simply doesn't pick up ambient acoustic noise. *(Figure cited from PMUT-based BC microphone study, PMC 2025 — not from TRAMBA)*

---

## Restricting Frequency Range: What You Miss

### Band-by-Band Breakdown

*Note: Human intelligibility figures below ~4 kHz are estimates synthesised from the research literature on narrowband speech perception; they are not single measured values and will vary by listener, noise conditions, and speech content.*

| Bandwidth Cutoff | What's Preserved | What's Lost | Human Intelligibility (est.) | STT Viability |
|---|---|---|---|---|
| Full (0–20 kHz) | Everything | Nothing | ~100% | Excellent |
| 0–8 kHz | All speech energy | Upper overtones in singing | ~99% | Excellent |
| 0–4 kHz | All vowels, voiced + most unvoiced consonants | Upper fricative sharpness | ~90–95% | Good |
| 300–3,400 Hz (telephone) | Vowels + key consonants | /s/, /f/ detail, some F0 cues | ~85–95% | Good *if model is trained on narrowband* |
| 0–2,500 Hz (bone conduction) | Vowels, voiced consonants, F0 | Fricatives, consonant detail | ~60–80% (context helps fill gaps) | Difficult without BC-specific model |
| 0–1,000 Hz | Vowels, prosody, pitch | All consonant distinction | ~20–40% | Fails |
| 0–500 Hz | Pitch, rhythm only | Everything lexical | <10% | Completely fails |

### The Specific Sounds You Lose at Each Cutoff

**Cutting above 4 kHz:** "s" loses its sharpness and "sh" becomes ambiguous. Singing loses brilliance.

**Cutting above 3.4 kHz (telephone):** Distinguishing /s/ from /f/, or /p/ from /t/ becomes harder. Intelligibility still high for connected speech in quiet.

**Cutting above 2.5 kHz (BC territory):** You lose the critical consonant distinction zone. "bat" vs. "pat", "see" vs. "fee" become ambiguous. Proper nouns and numbers become very unreliable. Humans compensate with context; STT cannot.

**Cutting above 1 kHz:** Almost all consonant distinction gone. You can hear that someone is speaking and follow prosody, but not understand words. STT fails.

**Cutting above 500 Hz:** Only pitch and rhythm remain. Completely useless for STT.

---

## STT: The Minimum Viable Frequency Range

### Practical Minimums

The practical STT bandwidth minimum is **300–3,400 Hz**, with an **8,000 Hz sample rate** (4,000 Hz Nyquist limit) being the absolute floor for acceptable performance.

> [!note] The Classic Call Center Standard
> Telephone networks at 300–3,400 Hz bandwidth have powered STT for call centers for decades. Accuracy is lower than wideband audio but is functional — especially when the **model is trained on matching narrowband data**.

### Google's Recommendation

Google Cloud Speech-to-Text documentation explicitly states: a sample rate below **16 kHz** results in audio with "little or no information above 8 kHz" — though in practice almost all speech energy worth transcribing is below 8 kHz. The concern is more about model expectation mismatch than missing acoustic content.

### The Critical Insight: Training Data Must Match

> [!important]
> Models trained on **wideband (16 kHz) audio** perform noticeably worse on **8 kHz narrowband** input — not because the information is gone, but because they weren't trained on that distribution.
>
> **Training data bandwidth matching matters as much as the actual captured bandwidth.**

### BC + STT: The State of the Art (2024–2025)

| Approach | STT Accuracy |
|---|---|
| Raw BC audio → generic STT (Whisper, Google, etc.) | ~65% WER — essentially unusable (TRAMBA paper, Table 5) |
| BC audio + **bandwidth expansion model (user fine-tuned)** → STT | 2.65% WER on BCM, 7.76% WER on ACCEL (TRAMBA, Whisper backend) |
| BC audio + **bandwidth expansion model (no fine-tuning)** → STT | ~34–65% WER — poor; generalizable models don't yet exist |
| BC + air mic **fusion** → STT | Best in quiet-to-moderate noise; BC provides noise immunity, AC provides full spectrum |

> [!tip]
> 2024 research from Northwestern specifically worked on **"bandwidth expansion" (audio super-resolution)** to reconstruct missing high-frequency content from BC signals *before* feeding them into STT — restoring much of the lost intelligibility.

---

## Deep Dive: BC Attenuation Measurements & Modern Enhancement

### Quantified Attenuation by Frequency

Research has produced actual measured dB numbers for how much BC attenuates speech at different frequencies:

| Frequency Range | Attenuation (approx.) | Effect |
|---|---|---|
| 100–600 Hz | Near-zero | Signal passes almost intact |
| 600–4,000 Hz | **5–10 dB loss** | Moderate degradation; intelligibility suffers |
| 3,000–5,000 Hz | **~10 dB** (mastoid position) | Consonant detail significantly degraded |
| Above 4,000 Hz | **Severe / highly variable** | High disturbance; effectively unusable |
| Transcutaneous path | Up to **20–25 dB** from skin alone | Passive devices through skin lose enormous signal strength |

> [!warning] Soft Tissue Thickness is the Key Variable
> Attenuation is not fixed — it scales directly with the thickness of soft tissue at the sensor placement site. Thicker tissue = more high-frequency loss. This is why placement matters enormously.

### Placement Location: How Much It Changes the Spectrum

The placement of a BC microphone on the body is one of the most consequential choices:

| Placement | Soft Tissue Thickness | High-Freq Attenuation | Similarity to Air Mic |
|---|---|---|---|
| **Forehead** | Thin | Lowest | **Most similar** to air conduction recording |
| **Mastoid** (behind ear) | ~11 mm | Moderate — ~10 dB at 3–5 kHz | Good |
| **Frontal/temporal** (in front of ear) | ~25 mm | ~20 dB more than mastoid at 10 kHz | Fair |
| **Throat / larynx** | Moderate | Higher — more tissue path | Poor |
| **Collarbone** | Most tissue path | Highest | **Most different** from air conduction |

> [!tip] Practical Takeaway
> **Forehead placement** gives the most spectrally complete BC signal per the BC mic placement study. **Mastoid** (behind the ear) is the standard clinical placement and a good compromise. Throat and collar placements maximally attenuate high frequencies.
>
> Note: The TRAMBA paper found **nasal bone (nose bridge)** to be the most consistent placement across participants for their specific sensor and wearable prototype. The "best" placement is sensor-dependent and may differ across hardware designs.

### Why Soft Tissue Thickness Is the Dominant Factor

A finding from bone conduction transmission studies: as soft tissue thickness increases, attenuation that starts at high frequencies progressively extends into **mid- and low-frequency regions** too. *(The specific 0–9 mm thickness range cited in some secondary sources is approximate and sensor/location-dependent; exact values vary by study.)* This means that at extreme tissue thicknesses, even the normally-preserved 500–1,500 Hz range begins to suffer. This is relevant for wearables placed over thick body areas.

---

## Modern BC Speech Enhancement: Research Landscape

### TRAMBA (2024, Sui, Zhao, Xia et al. — Northwestern & Columbia)

*Published in Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., Vol. 8, No. 4, Article 205 (December 2024)*

TRAMBA (**TR**ansformer **A**nd **M**am**B**a **A**rchitecture — *acronym interpreted; paper does not explicitly expand it*) is designed specifically for practical, real-time BC speech super-resolution on mobile and wearable hardware. It is the most comprehensive and rigorous study of BC speech enhancement published to date.

#### The Exact Task Being Solved

BCMs and accelerometers (ACCELs) sampled at **4kHz contain no energy above 2kHz** — confirmed directly by spectrograms in the paper (Fig. 3, Fig. 10). The task is upsampling from 4kHz to 16kHz: reconstructing the **2kHz–8kHz band** that is entirely absent in BC/ACCEL recordings.

```
BCM/ACCEL input (4kHz sampled):  ████████▓▓░░░░░░  (energy only 0–2kHz)
OTA microphone (16kHz sampled):  ████████████████  (energy 0–8kHz+)

TRAMBA's job:                    reconstruct ████████ (2kHz–8kHz)
                                             from just ████████ (0–2kHz input)
```

#### Architecture (from paper)

The model is a modified U-Net with 3 downsampling + 3 upsampling blocks, with Mamba in the bottleneck:

- **Downsampling blocks:** 1D Conv → LeakyReLU → SAFiLM. Kernel sizes: 65, 17, 7. Filters: 2^(5+b).
- **Bottleneck:** Mamba (structured state space model). Chosen over Transformer because it matches Transformer performance at half the memory. Gradient vanishing found when using Mamba in all layers, so SAFiLM Transformers are retained in the contracting/expanding blocks.
- **Upsampling blocks:** Conv → Dropout → LeakyReLU → Pixelshuffle (1D) → SAFiLM.
- **SAFiLM** (Scale-only Attention-based Feature-wise Linear Modulation) — a novel contribution. A memory-efficient variant of AFiLM that learns only a scaling factor γ (not a shift β), computed by a Transformer block over max-pooled features. This captures long-range speech structure at each abstraction level while keeping memory small.
- **Residual connections** (not skip concatenations) — allows gradients to flow, reduces vanishing gradient risk.
- **Input:** 512ms windows of single-channel audio.
- **Parameters:** 5.2 million.

#### Training Pipeline

**Phase 1 — Pre-training on OTA audio (VCTK dataset):**
- 109 native English speakers, ~44 hours of clean speech
- 100 speakers for training, 9 for testing
- Input: clean speech downsampled to 4kHz. Target: same speech at 16kHz
- Loss function: MAE + multi-resolution STFT loss (FFT bins ∈ {512, 1024, 2048})
- 30 epochs to convergence

**Phase 2 — Fine-tuning on user's BC data:**
- User simultaneously records OTA speech (via phone mic) + BC/ACCEL (via wearable) for ~15 minutes
- Pre-trained model is fine-tuned on these paired examples
- Fine-tuning hardware: NVIDIA L40 GPU (transmitted via BLE to phone, then to GPU)
- Inference runs locally on phone after model is pushed back

#### Performance: OTA Super Resolution (4kHz → 16kHz, Table 1)

All models compared on the VCTK test set. Higher PESQ/STOI = better. Lower LSD = better.

| Method | Params | Size (MB) | Inference (ms) | PESQ | STOI | LSD |
|---|---|---|---|---|---|---|
| Raw 4kHz audio (baseline) | — | — | — | 1.87 | 0.82 | 2.49 |
| TFiLM (U-Net) | 68.2M | 260.3 | 4.6 | 2.43 | 0.85 | 1.87 |
| AFiLM (U-Net) | 134.7M | 513.9 | 5.6 | 2.47 | 0.87 | 1.87 |
| TUNet (U-Net) | 2.9M | 11.2 | 2.8 | 2.58 | 0.94 | 0.94 |
| ATS-UNet (U-Net) | 0.1M | 0.5 | 3.4 | 1.55 | 0.70 | 1.56 |
| EBEN (GAN) | 29.7M | 113.3 | 242.1 | 2.58 | 0.89 | 1.08 |
| Aero (GAN) | 36.3M | 138.7 | **1084.5** | 3.01 | 0.94 | **0.81** |
| **TRAMBA** | **5.2M** | **19.7** | **2.33** | **3.23** | **0.95** | 0.83 |

Key observations: TRAMBA beats the best GAN (Aero) on PESQ and STOI while being **465× faster** (2.33ms vs 1084.5ms) and using **7× less memory** (19.7MB vs 138.7MB). Aero is the only model that slightly beats TRAMBA on LSD (signal similarity), but LSD doesn't capture perceptual quality as well as PESQ/STOI.

#### Performance: BC/ACCEL Enhancement (4kHz → 16kHz, fine-tuned, Table 3 & 4)

Fine-tuned on 15 minutes of data at Nasal Bone (Location 2). All metrics below are from Table 4 (52-minute fine-tuning cap, same experimental condition). WER computed by feeding output into **Whisper** (OpenAI's STT model). TRAMBA's numbers are identical across both table conditions because it converges within 34 minutes.

**BCM results:**

| Method | PESQ | STOI | LSD | WER (Whisper) | Fine-tune time/epoch |
|---|---|---|---|---|---|
| TFiLM | 2.14 | 0.88 | 1.33 | 8.73% | 24.6s |
| AFiLM | 2.26 | 0.88 | 1.47 | 6.48% | 28.5s |
| TUNet | 1.92 | 0.87 | 1.12 | 6.21% | 2.6s |
| ATS-UNet | 1.42 | 0.74 | 1.54 | 29.86% | 12.9s |
| Aero (GAN) | 2.67 | 0.91 | 0.89 | 4.48% | 29.7s |
| **TRAMBA** | **2.73** | **0.92** | **0.93** | **2.65%** | **1.6s** |

**ACCEL results:**

| Method | PESQ | STOI | LSD | WER (Whisper) |
|---|---|---|---|---|
| TFiLM | 1.66 | 0.85 | 1.52 | 12.89% |
| TUNet | 1.63 | 0.84 | 1.46 | 13.29% |
| Aero (GAN) | 2.02 | 0.90 | 1.11 | 14.04% |
| **TRAMBA** | **2.14** | **0.92** | **1.03** | **7.76%** |

> [!success] TRAMBA achieves **2.65% WER on BCM** and **7.76% WER on ACCEL** when fine-tuned on 15 minutes of personal data, with fine-tuning taking only **34 minutes** (BCM) / **43 minutes** (ACCEL) to convergence — orders of magnitude faster than competing methods (Aero takes 1,370 minutes).

#### The Critical Finding: You MUST Fine-Tune on BC Data (Table 5)

This is the most important practical finding in the paper:

| Training approach | BCM WER | ACCEL WER |
|---|---|---|
| Pre-trained on OTA audio only, no BC fine-tuning | **65.51%** | **33.33%** |
| Generalizable model (trained on 6 users, tested on unseen 7th) | 34.67% | 44.52% |
| Fine-tuned to the specific individual (15 min) | **2.65%** | **7.76%** |

Without user-specific fine-tuning, BCM audio fed to Whisper gives **65% word error rate**. Fine-tuning to the individual drops it to 2.65%. This explains why off-the-shelf STT on raw BC audio fails so catastrophically: the spectral distortion profile is both user-specific and placement-specific, and no generalizable model exists yet.

#### Real-World STT Performance in Noisy Environments (Table 7)

This is the most striking result. WER across real environments using Whisper as the STT backend:

| Method | Cafeteria (SNR −0.4 dB) | Loud Music (SNR −3.7 dB) | Construction Site (SNR −10.5 dB) |
|---|---|---|---|
| Raw OTA audio | 15.85% | 45.12% | 86.59% |
| Conv-TasNet (OTA denoising) | 79.88% | 20.12% | 85.37% |
| DCUNet (OTA denoising) | 17.07% | 83.54% | 86.59% |
| **TRAMBA-BCM** | **7.93%** | **6.10%** | **14.63%** |
| **TRAMBA-ACCEL** | **4.27%** | **16.46%** | **10.37%** |

At a construction site with **−10.5 dB SNR** (noise is 10× louder than speech), raw OTA audio gives 86.59% WER — essentially unusable. TRAMBA-BCM achieves **14.63%** and TRAMBA-ACCEL achieves **10.37%**. OTA denoising methods (Conv-TasNet, DCUNet) fail completely in these conditions.

#### Sensor Placement Results (Fig. 11)

The paper tested 5 placement locations on the face. Nasal bone (nose bridge) gave the most consistent performance across users and was chosen as the primary test site.

| Location | Bone |
|---|---|
| 1 — Cheekbone (near ear) | Temporal Bone |
| **2 — Nose** | **Nasal Bone (best overall)** |
| 3 — Chin | Mandible |
| 4 — Below Eye | Zygomatic Bone |
| 5 — Back of Head | Parietal Bone |

TRAMBA maintained consistently better performance across **all** placements vs. competing methods.

#### Effect of Input Sampling Rate (Section 5.3.5, Fig. 15)

The paper explicitly tested TRAMBA's performance as input sampling rate varies from 500Hz to 4kHz:

- TRAMBA achieves **acceptable quality from ~2kHz input** for both BCM and ACCEL
- TUNet needs at least **double TRAMBA's sampling rate** to achieve similar performance
- Even at 500Hz input, TRAMBA outperforms TUNet at 4kHz — meaning TRAMBA can use less data and still win

> [!tip] Practical Implication
> You can sample a BCM at 2kHz (capturing 0–1kHz), run TRAMBA, and get better STT results than competing models operating at 4kHz input.

#### Power Consumption and Latency (Tables 9 & 10)

Sampling the BCM/ACCEL at 4kHz instead of full 16kHz OTA cuts data transmission and power dramatically:

| Configuration | Data Rate | Power Consumption |
|---|---|---|
| TRAMBA at 500Hz | 8 kbps | 2.49 mW |
| TRAMBA at 1kHz | 16 kbps | 2.58 mW |
| TRAMBA at 2kHz | 32 kbps | 2.75 mW |
| **TRAMBA at 4kHz** | **64 kbps** | **3.21 mW** |
| TRAMBA at 8kHz | 128 kbps | 4.09 mW |
| No enhancement (16kHz OTA) | 256 kbps | 6.48 mW |

Sampling at 4kHz vs full 16kHz OTA: **75% less data**, **>50% power reduction** from sampling+transmission.

**Inference latency on phones (512ms window):**

| Device | Inference time |
|---|---|
| iPhone 15 Pro | 19.6 ms |
| iPhone 14 Pro | 20.3 ms |
| iPhone 13 Pro | 23.0 ms |
| iPhone 12 | 27.9 ms |

All under 30ms for a 512ms window → **fully real-time** on modern smartphones.

#### Movement Robustness (Section 7.2, Fig. 17)

Movement artefacts (walking, running) appear in BCM/ACCEL at frequencies **well below 100Hz** — in the single Hz range. A simple **first-order Butterworth high-pass filter at 10Hz** removes them entirely. Performance metrics while walking at 1.2 m/s are virtually identical to stationary.

#### Gender Difference

Performance was consistently **lower for female voices than male voices** across all methods. The paper hypothesises this is because higher-pitched voices have energy at higher frequencies, which experience greater attenuation through bone and skin. Identified as an open research problem.

#### Data Requirements

- With **only 2 minutes** of personal BC data, TRAMBA outperforms TUNet fine-tuned on 15 minutes
- With **2.6 minutes** (100 epochs) of training, TRAMBA surpasses TUNet trained for 52 minutes on most metrics
- Creating a **generalizable** model that works on unseen individuals without fine-tuning remains unsolved

#### Hardware Used in the Study

- **BCM:** Knowles V2S200D voice vibration sensor
- **ACCEL:** InvenSense IIM-42352 MEMS accelerometer
- **Wearable SoC:** Seeed Studio XIAO nRF52840 BLE (transmits via Bluetooth LE to phone)
- **Fine-tuning GPU:** NVIDIA L40
- **Model deployment:** PyTorch → ONNX → TensorFlow Lite (tflite) for smartphone inference

---

## BC Frequency Enhancement: What's Actually Being Reconstructed

This is the concrete picture of the super-resolution task as established by the TRAMBA paper's spectrograms:

```
Sensor input (BCM/ACCEL sampled at 4kHz):
  0──────────2kHz──────────8kHz
  ████████████░░░░░░░░░░░░░░░░   ← energy only below 2kHz, black above

OTA microphone ground truth (16kHz):
  0──────────2kHz──────────8kHz
  ████████████████████████████   ← full energy across spectrum

TRAMBA output (reconstructed):
  0──────────2kHz──────────8kHz
  ████████████████████████████   ← 2–8kHz band hallucinated from 0–2kHz input
```

The models learn to reconstruct high-frequency speech formants from low-frequency structure. This works because speech is highly constrained — the harmonics and formants in 0–2kHz strongly predict what the 2–8kHz content must look like for a given phoneme and speaker. The 15 minutes of fine-tuning data teaches the model your specific voice's spectral signature; the pre-training teaches it the general rules of speech physics.

> [!warning] Without fine-tuning, a model pre-trained on OTA audio applied directly to raw BCM achieves 65% WER on Whisper — essentially unusable for STT. Fine-tuning to the individual is not optional; it is the entire difference between failure and success.

### BC + Air Conduction Fusion (Alternative Approach)

Several other papers propose fusing BC and air conduction (AC) signals rather than reconstructing from BC alone. This sidesteps the hallucination problem entirely: BC provides a clean low-frequency signal, AC provides the full spectrum but picks up noise. At high noise levels, BC is weighted more; at low noise, AC is weighted more. Best suited to environments where an OTA mic is also available (e.g. headset with both sensors).

---

## Quick Reference: Frequency Map of Human Voice

```
Hz:    100   250   500   1k    2k    4k    8k    16k   20k
        |     |     |     |     |     |     |     |     |
F0 (M)  ████
F0 (F)        ████
Vowels        ███████████
Voiced C      ██████████████████
Unvoiced C               ████████████████
Fricatives               ████████████████████████
Singing F0    ████████████
Harmonics     ████████████████████████████████████████
Singer'sF           ████████
BC limit  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Telephone     ████████████
```

---

## Sources

**Voice & Speech Fundamentals**
- [Formant — Wikipedia](https://en.wikipedia.org/wiki/Formant)
- [Voice Frequency — Wikipedia](https://en.wikipedia.org/wiki/Voice_frequency)
- [The Perceptual Significance of High-Frequency Energy in the Human Voice — Frontiers in Psychology](https://www.frontiersin.org/articles/10.3389/fpsyg.2014.00587/full)
- [Intelligibility vs. Bandwidth — Hearing Health Matters](https://hearinghealthmatters.org/waynesworld/2014/intelligibility-vs-bandwidth/)

**Singing Voice**
- [Singer's Formant — VoiceScience.org](https://www.voicescience.org/2025/11/lexicon/singers-formant/)
- [Voice Source, Formant Frequencies in Overtone Singing — Tandfonline](https://www.tandfonline.com/doi/full/10.1080/14015439.2021.1998607)

**Bone Conduction — Physics & Placement**
- [Bone Conduction — Wikipedia](https://en.wikipedia.org/wiki/Bone_conduction)
- [Effect of BC Mic Placement on Intelligibility and Sound Quality — ResearchGate](https://www.researchgate.net/publication/47383372_The_effect_of_bone_conduction_microphone_locations_on_speech_intelligibility_and_sound_quality)
- [Effect of BC Mic Placement on Intensity and Spectrum — ResearchGate](https://www.researchgate.net/publication/237068684_The_effect_of_bone_conduction_microphone_placement_on_intensity_and_spectrum_of_transmitted_speech_items)
- [Comparison of Bone-Conduction Technologies — US DTIC / Military Research](https://apps.dtic.mil/sti/pdfs/ADA499561.pdf)
- [PMUT-Based Bone Conduction Microphone for Enhancing Speech Recognition — PMC 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12195400/)

**Bone Conduction — Enhancement & Super Resolution**
- [TRAMBA: Hybrid Transformer and Mamba Architecture for BC Super Resolution — ACM IMWUT 2024](https://dl.acm.org/doi/10.1145/3699757) *(Sui, Zhao, Xia, Jiang, Xia — Northwestern & Columbia)*
- [TRAMBA open-source code and data](https://imec-northwestern.github.io/TRAMBAPage/)
- [Improving Acoustic and Bone Conduction Speech Enhancement — Northwestern Engineering News, 2024](https://www.mccormick.northwestern.edu/news/articles/2024/12/improving-acoustic-and-bone-conduction-speech-enhancement/)
- [Enabling Real-Time On-Chip Audio Super Resolution for BC Microphones — PMC / Sensors 2023](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9823296/)
- [Bandwidth Extension WaveNet for Bone-Conducted Speech Enhancement — SpringerLink](https://link.springer.com/chapter/10.1007/978-981-15-2756-2_1)
- [Fusing Bone-Conduction and Air-Conduction Sensors for Speech Enhancement — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10147322/)
- [Enhancing Bone-Conducted Speech via Pre-Trained Transformer with Low-Rank Sparsity — SSRN (Shan, Yang et al.)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4991984)
- [Personalized Bone-Conduction Bandwidth Extension with Speaker Characteristics — APSIPA 2025](http://www.apsipa.org/proceedings/2025/papers/APSIPA2025_P491.pdf)
- [Regional Language Speech Recognition from Bone Conducted Speech — Springer 2024](https://link.springer.com/article/10.1007/s00034-024-02733-y)

**STT & Frequency Bandwidth**
- [Optimize Audio for Cloud Speech-to-Text — Google Cloud](https://docs.cloud.google.com/speech-to-text/docs/v1/optimizing-audio-files-for-speech-to-text)
- [2025 STT Accuracy Benchmark for 8 kHz Call Center Audio — Voicegain](https://www.voicegain.ai/post/2025-speech-to-text-accuracy-benchmark-for-8-khz-call-center-audio-files)

---
*Created: 2026-03-18*
