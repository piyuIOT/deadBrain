"""
Hard Negative Audio Generator
==============================
Reads wake_words negatives from stt_corpus.json and generates
synthesised audio clips.

Engines (tries in order):
  1. Piper TTS  — fully offline, multiple voices, same engine openWakeWord uses
                   Voices auto-downloaded on first run from HuggingFace (~50MB each)
  2. gTTS        — fallback, requires internet, Google TTS

Output structure:
  hard_negatives/
    WKW-001_Hey_Temple/
      WKW-001-NEG-001_amy_1.00x.wav
      WKW-001-NEG-001_amy_0.85x.wav
      WKW-001-NEG-001_ryan_1.00x.wav
      ...
    WKW-002_OK_Temple/
      ...

Usage:
  python3 generate_hard_negatives.py                          # all wake words
  python3 generate_hard_negatives.py --wkw WKW-001           # one wake word
  python3 generate_hard_negatives.py --wkw WKW-001 WKW-002   # multiple
  python3 generate_hard_negatives.py --engine gtts            # force gTTS
  python3 generate_hard_negatives.py --no-augment             # no speed variants
  python3 generate_hard_negatives.py --speeds 0.85 1.0 1.15  # custom speeds

Requirements:
  pip install piper-tts pathvalidate pydub gtts --break-system-packages
"""

import json
import os
import sys
import argparse
import subprocess
import time
import urllib.request
from pathlib import Path


# ── Config ────────────────────────────────────────────────────────────────────

CORPUS_FILE  = Path(__file__).parent / "stt_corpus.json"
OUTPUT_DIR   = Path(__file__).parent / "hard_negatives"
VOICES_DIR   = Path(__file__).parent / "piper_voices"

DEFAULT_SPEEDS = [0.85, 1.0, 1.15]

# Piper voices to use — covers US male, US female, UK male, UK female
# Full list: https://huggingface.co/rhasspy/piper-voices/tree/main/en
PIPER_VOICES = {
    "en_US-amy-medium":   "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx",
    "en_US-ryan-high":    "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ryan/high/en_US-ryan-high.onnx",
    "en_GB-alba-medium":  "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alba/medium/en_GB-alba-medium.onnx",
    "en_GB-alan-medium":  "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_GB/alan/medium/en_GB-alan-medium.onnx",
}

PIPER_VOICE_CONFIGS = {
    k: v.replace(".onnx", ".onnx.json") for k, v in PIPER_VOICES.items()
}

# gTTS accent variants (fallback engine)
GTTS_ACCENTS = {
    "us":  ("en", "com"),
    "uk":  ("en", "co.uk"),
    "au":  ("en", "com.au"),
    "in":  ("en", "co.in"),
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_corpus(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def safe_name(text: str, max_len: int = 35) -> str:
    clean = "".join(c if c.isalnum() or c in " _-" else "" for c in text)
    return clean.strip().replace(" ", "_")[:max_len]


def progress(i: int, n: int, label: str = "") -> None:
    filled = int(28 * i / n)
    bar    = "█" * filled + "░" * (28 - filled)
    print(f"\r  [{bar}] {i}/{n}  {label:<38}", end="", flush=True)


# ── Piper engine ──────────────────────────────────────────────────────────────

def piper_available() -> bool:
    try:
        import piper as _  # noqa
        result = subprocess.run(
            ["piper", "--help"], capture_output=True, timeout=5
        )
        return True
    except Exception:
        return False


def download_voice(voice_name: str) -> tuple[Path, Path] | None:
    """Download a piper voice .onnx + .onnx.json if not already present."""
    VOICES_DIR.mkdir(parents=True, exist_ok=True)
    onnx_url   = PIPER_VOICES[voice_name]
    config_url = PIPER_VOICE_CONFIGS[voice_name]
    onnx_path  = VOICES_DIR / f"{voice_name}.onnx"
    cfg_path   = VOICES_DIR / f"{voice_name}.onnx.json"

    for url, dst in [(onnx_url, onnx_path), (config_url, cfg_path)]:
        if not dst.exists():
            print(f"  Downloading {dst.name} ...", end=" ", flush=True)
            try:
                urllib.request.urlretrieve(url, dst)
                print("done")
            except Exception as e:
                print(f"FAILED: {e}")
                return None
    return onnx_path, cfg_path


def generate_piper(text: str, voice_name: str, onnx_path: Path, cfg_path: Path, out_path: Path) -> bool:
    """Generate audio with Piper via subprocess."""
    try:
        result = subprocess.run(
            [
                "piper",
                "--model", str(onnx_path),
                "--config", str(cfg_path),
                "--output_file", str(out_path),
            ],
            input=text,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return out_path.exists() and out_path.stat().st_size > 0
    except Exception as e:
        print(f"\n    ✗ Piper error ({voice_name}): {e}")
        return False


# ── gTTS engine ───────────────────────────────────────────────────────────────

def generate_gtts(text: str, lang: str, tld: str, out_path: Path) -> bool:
    try:
        from gtts import gTTS
        gTTS(text=text, lang=lang, tld=tld, slow=False).save(str(out_path))
        return True
    except Exception as e:
        print(f"\n    ✗ gTTS error ({tld}): {e}")
        return False


# ── Speed augmentation ────────────────────────────────────────────────────────

def augment_speed(src: Path, speed: float, dst: Path) -> bool:
    try:
        from pydub import AudioSegment
        fmt = src.suffix.lstrip(".")
        audio = AudioSegment.from_file(str(src), format=fmt)
        shifted = audio._spawn(
            audio.raw_data,
            overrides={"frame_rate": int(audio.frame_rate * speed)}
        ).set_frame_rate(audio.frame_rate)
        shifted.export(str(dst), format=fmt)
        return True
    except Exception as e:
        print(f"\n    ✗ Speed aug error ({speed}x): {e}")
        return False


# ── Main generation ───────────────────────────────────────────────────────────

def run(wkw_filter, speeds, no_augment, engine):
    corpus    = load_corpus(CORPUS_FILE)
    wakewords = corpus.get("wake_words", [])

    if not wakewords:
        print("No wake_words in corpus."); return

    if wkw_filter:
        wakewords = [w for w in wakewords if w["id"] in wkw_filter]
        if not wakewords:
            print(f"No matches for {wkw_filter}"); return

    # ── Decide engine ──────────────────────────────────────────────────────
    use_piper = False
    piper_voice_files = {}

    if engine != "gtts" and piper_available():
        print("  Engine: Piper TTS (offline)\n  Downloading any missing voices...")
        for vname in PIPER_VOICES:
            result = download_voice(vname)
            if result:
                piper_voice_files[vname] = result
        if piper_voice_files:
            use_piper = True
            print(f"  Ready voices: {', '.join(piper_voice_files.keys())}")
        else:
            print("  Piper voice download failed — falling back to gTTS")

    if not use_piper:
        print("  Engine: gTTS (requires internet)")
        try:
            import gtts as _  # noqa
        except ImportError:
            print("ERROR: neither piper nor gtts available.")
            print("  Install: pip install piper-tts pathvalidate gtts --break-system-packages")
            sys.exit(1)

    total = skipped = failed = 0

    for wkw in wakewords:
        wkw_id    = wkw["id"]
        phrase    = wkw["phrase"]
        negatives = wkw.get("negatives", [])

        if not negatives:
            print(f"\n{wkw_id} ({phrase}) — no negatives, skipping."); continue

        folder = OUTPUT_DIR / f"{wkw_id}_{safe_name(phrase)}"
        folder.mkdir(parents=True, exist_ok=True)

        print(f"\n{'─'*62}")
        print(f"  {wkw_id}  \"{phrase}\"  — {len(negatives)} negatives")
        print(f"  → {folder}")
        print(f"{'─'*62}")

        for i, neg in enumerate(negatives, 1):
            neg_id = neg["id"]
            text   = neg["text"]
            progress(i, len(negatives), neg_id)

            if use_piper:
                # ── Piper: one clip per voice ──────────────────────────
                for vname, (onnx, cfg) in piper_voice_files.items():
                    base = folder / f"{neg_id}_{vname}_1.00x.wav"
                    if base.exists():
                        skipped += 1
                    else:
                        ok = generate_piper(text, vname, onnx, cfg, base)
                        (total if ok else failed).__add__(0)  # count
                        if ok: total += 1
                        else:  failed += 1

                    if not no_augment and base.exists():
                        for spd in speeds:
                            if spd == 1.0: continue
                            dst = folder / f"{neg_id}_{vname}_{spd:.2f}x.wav"
                            if dst.exists():
                                skipped += 1
                            else:
                                ok = augment_speed(base, spd, dst)
                                if ok: total += 1
                                else:  failed += 1

            else:
                # ── gTTS: one clip per accent ──────────────────────────
                for accent, (lang, tld) in GTTS_ACCENTS.items():
                    base = folder / f"{neg_id}_{accent}_1.00x.mp3"
                    if base.exists():
                        skipped += 1
                    else:
                        ok = generate_gtts(text, lang, tld, base)
                        if ok: total += 1
                        else:  failed += 1
                        time.sleep(0.3)  # avoid rate limit

                    if not no_augment and base.exists():
                        for spd in speeds:
                            if spd == 1.0: continue
                            dst = folder / f"{neg_id}_{accent}_{spd:.2f}x.mp3"
                            if dst.exists():
                                skipped += 1
                            else:
                                ok = augment_speed(base, spd, dst)
                                if ok: total += 1
                                else:  failed += 1

        print()

    print(f"\n{'═'*62}")
    print(f"  Generated : {total}   Skipped: {skipped}   Failed: {failed}")
    print(f"  Output    : {OUTPUT_DIR}")
    print(f"{'═'*62}\n")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate synthesised hard negative audio for wake word training."
    )
    parser.add_argument("--wkw", nargs="+", metavar="ID",
        help="Wake word IDs to process (default: all)")
    parser.add_argument("--speeds", nargs="+", type=float, default=DEFAULT_SPEEDS,
        help=f"Speed multipliers (default: {DEFAULT_SPEEDS})")
    parser.add_argument("--no-augment", action="store_true",
        help="Skip speed augmentation")
    parser.add_argument("--engine", choices=["auto", "piper", "gtts"], default="auto",
        help="TTS engine to use (default: auto — tries piper first)")

    args = parser.parse_args()
    print(f"\n  Hard Negative Generator")
    print(f"  Corpus : {CORPUS_FILE}")
    print(f"  Speeds : {args.speeds if not args.no_augment else 'disabled (--no-augment)'}\n")

    run(args.wkw, args.speeds, args.no_augment, args.engine)


if __name__ == "__main__":
    main()
