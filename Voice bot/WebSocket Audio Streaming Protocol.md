# Current State (v2.1.1)
## What format is used now?

| Direction           | Format                                   | Details                                                 |
| ------------------- | ---------------------------------------- | ------------------------------------------------------- |
| **Mic → Server**    | Raw 16-bit PCM, 16 kHz, **stereo (2ch)** | Sent as binary WebSocket frames                         |
| **Server → Device** | Raw 16-bit PCM, assumed 16 kHz mono      | Received as binary, cast to `int16_t*`, played directly |
## Problems
1. **Sending stereo interleaved data** — The capture task reads from I2S in stereo
   (MIC1 + MIC2 interleaved) and the `on_audio_data()` callback sends the raw
   buffer straight to `app_ws_send_audio()` without downmixing to mono. The
   server would receive L,R,L,R,L,R… interleaved samples, doubling bandwidth
   for no benefit.
2. **No format metadata** — The server has no way to know the sample rate,
   bit depth, or channel count. If the NVS `sample_rate` setting changes
   (16000 / 22050 / 44100), the binary stream silently becomes incompatible.
3. **No selectable format** — There's no handshake or configuration message
   to let either side agree on a format.
4. **Receive path assumes raw PCM** — `on_ws_audio()` casts `uint8_t*` to
   `int16_t*` and feeds it straight to the DAC at whatever rate the codec is
   currently set to. No sample-rate conversion if the server sends at a
   different rate.
---
# Proposed Protocol (standalone design — not merged into v2.1.1)
## 1. Session Handshake
On WebSocket connect, the **device sends** a JSON text frame:
```json
{
  "event": "session_start",
  "audio": {
    "format": "pcm_s16le",
    "sample_rate": 16000,
    "channels": 1,
    "frame_size_ms": 200
  },
  "device": {
    "name": "VoiceBot-S3",
    "version": "2.1.1",
    "mics": 2
  }
}
```

The **server responds** with its preferred playback format:
```json
{
  "event": "session_ack",
  "audio": {
    "format": "pcm_s16le",
    "sample_rate": 16000,
    "channels": 1
  }
}
```
## 2. Audio Frames (binary)
All binary WebSocket frames carry a tiny 4-byte header followed by PCM data:
```
Byte 0:  Frame type   0x01 = mic audio, 0x02 = playback audio
Byte 1:  Flags        bit 0 = last frame of utterance
Byte 2-3: Sequence number (uint16_t little-endian, wraps at 65535)
Byte 4+: Raw PCM samples (16-bit signed little-endian, mono)
```

**Mic → Server** (type 0x01):
- Device downmixes stereo to mono before sending
- 16 kHz, 16-bit signed LE, 1 channel
- ~200 ms per frame = 3200 samples = 6400 bytes + 4 header = **6404 bytes/frame**
- Last frame flagged with `flags |= 0x01`

**Server → Device** (type 0x02):
- Server sends mono 16 kHz 16-bit PCM
- Device plays through ES8311 DAC
- Last frame flagged with `flags |= 0x01` to signal end-of-response
## 3. Text Control Messages

| Sender | Event | Purpose |
|--------|-------|---------|
| Device | `{"event":"session_start","audio":{...}}` | Negotiate format |
| Server | `{"event":"session_ack","audio":{...}}` | Confirm format |
| Device | `{"event":"listening_start"}` | Talk button pressed |
| Device | `{"event":"end_of_speech"}` | Talk button released / VAD triggered |
| Server | `{"event":"thinking"}` | Server processing |
| Server | `{"event":"response_start"}` | Audio/text response starting |
| Server | `{"event":"response_text","text":"Hello!"}` | AI text reply |
| Server | `{"event":"response_end"}` | Full response delivered |
| Either | `{"event":"ping"}` / `{"event":"pong"}` | Keep-alive |

---
# Implementation Plan (separate from main codebase)
## File: `ws_audio_proto.h` / `ws_audio_proto.c`
A drop-in helper module that wraps `app_ws_client` with proper framing:
```c
/* ── ws_audio_proto.h ─────────────────────────────────────────────── */

#pragma once
#include <stdint.h>
#include <stddef.h>
#include "esp_err.h"

/* Audio format descriptor */
typedef struct {
    int      sample_rate;   /* 8000, 16000, 22050, 44100 */
    int      bits;          /* 16 */
    int      channels;      /* 1 (mono) or 2 (stereo) */
    int      frame_ms;      /* frame duration in ms (e.g. 200) */
} ws_audio_fmt_t;

/* Binary frame header (4 bytes) */
typedef struct __attribute__((packed)) {
    uint8_t  type;           /* 0x01=mic, 0x02=playback */
    uint8_t  flags;          /* bit0=last_frame */
    uint16_t seq;            /* sequence number LE */
} ws_audio_hdr_t;

#define WS_FRAME_MIC       0x01
#define WS_FRAME_PLAY      0x02
#define WS_FLAG_LAST        0x01

/**
 * Send session_start handshake with device's preferred format
 */
esp_err_t ws_proto_send_session_start(const ws_audio_fmt_t *fmt);

/**
 * Send a mic audio frame (stereo in → mono out, adds header)
 * @param stereo_pcm  Raw I2S stereo buffer (int16_t interleaved L,R,L,R...)
 * @param stereo_samples  Total sample count (includes both channels)
 * @param last  true if this is the last frame of the utterance
 */
esp_err_t ws_proto_send_mic_frame(const int16_t *stereo_pcm,
                                   size_t stereo_samples, bool last);

/**
 * Parse an incoming binary frame.
 * Returns header info + pointer to PCM payload.
 */
esp_err_t ws_proto_parse_frame(const uint8_t *data, size_t len,
                                ws_audio_hdr_t *hdr,
                                const int16_t **pcm_out,
                                size_t *pcm_samples);
```
## Key implementation details
### Stereo → Mono downmix before sending
```c
/* Inside ws_proto_send_mic_frame() */
size_t mono_count = stereo_samples / 2;
int16_t *mono = malloc(mono_count * sizeof(int16_t));
for (size_t i = 0; i < mono_count; i++) {
    int32_t mix = (int32_t)stereo_pcm[i*2] + (int32_t)stereo_pcm[i*2+1];
    mono[i] = (int16_t)(mix / 2);
}
/* Send header + mono buffer as single binary frame */
```
This halves the bandwidth from **12.8 KB/frame** (stereo) to **6.4 KB/frame** (mono).
### Selectable sample rate via NVS
The `app_settings_t.sample_rate` field already exists (supports 16000 / 22050 / 44100).

The protocol module reads this at session start:
```c
const app_settings_t *s = app_nvs_get();
ws_audio_fmt_t fmt = {
    .sample_rate = s->sample_rate,  // user-configurable
    .bits = 16,
    .channels = 1,                   // always send mono
    .frame_ms = 200,
};
ws_proto_send_session_start(&fmt);
```

The server knows exactly what it's receiving.
### Receive path — respect server format
When `session_ack` arrives, the device stores the server's format. On incoming
binary frames, if the server's sample rate differs from the codec's current
rate, the device calls `bsp_extra_codec_set_fs()` to switch the DAC before
playing:
```c
void on_ws_audio_frame(const ws_audio_hdr_t *hdr,
                        const int16_t *pcm, size_t samples) {
    if (server_fmt.sample_rate != current_dac_rate) {
        bsp_extra_codec_set_fs(server_fmt.sample_rate, 16, 1);
        current_dac_rate = server_fmt.sample_rate;
    }
    app_audio_play_pcm(pcm, samples);

    if (hdr->flags & WS_FLAG_LAST) {
        /* Restore mic sample rate on DAC */
        bsp_extra_codec_set_fs(mic_fmt.sample_rate, 16, I2S_SLOT_MODE_STEREO);
    }
}
```

---
# Bandwidth Summary

| Config                        | Per frame (200ms) | Per second | Notes                   |
| ----------------------------- | ----------------- | ---------- | ----------------------- |
| **16 kHz mono (recommended)** | 6,404 B           | 32 KB/s    | Good for speech AI      |
| 22.05 kHz mono                | 8,824 B           | 44 KB/s    | Better quality          |
| 44.1 kHz mono                 | 17,644 B          | 88 KB/s    | Overkill for speech     |
| 16 kHz stereo (current bug)   | 12,804 B          | 64 KB/s    | Wasteful, sends raw I2S |

**Recommendation: 16 kHz mono PCM** — standard for speech-to-text APIs
(Google, Whisper, Deepgram, Azure all expect 16 kHz mono).

---
# Server-Side Example (Python)

Minimal server to test the protocol:
```python
#!/usr/bin/env python3
"""ws_test_server.py — Test WebSocket server for Voice Bot Pro"""
import asyncio, json, struct
import websockets

async def handler(ws):
    print("Device connected")
    async for msg in ws:
        if isinstance(msg, str):
            data = json.loads(msg)
            event = data.get("event")
            print(f"Text: {event}")

            if event == "session_start":
                # Echo back the format we accept
                ack = {
                    "event": "session_ack",
                    "audio": data["audio"]
                }
                await ws.send(json.dumps(ack))

            elif event == "end_of_speech":
                # Send a text response
                resp = {"event": "response_text", "text": "I heard you!"}
                await ws.send(json.dumps(resp))

        elif isinstance(msg, bytes):
            # Binary frame: 4-byte header + PCM
            if len(msg) > 4:
                ftype, flags, seq = struct.unpack_from("<BBH", msg, 0)
                pcm = msg[4:]
                samples = len(pcm) // 2
                print(f"Audio frame: type={ftype:#x} seq={seq} "
                      f"samples={samples} last={bool(flags & 1)}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8080):
        print("WS server on ws://0.0.0.0:8080")
        await asyncio.Future()

asyncio.run(main())
```

Run: `pip install websockets && python ws_test_server.py`

Then configure the device:
- WebSocket URL: `ws://<your-pc-ip>:8080`
- Via the web dashboard at `http://voicebot.local`

---
# Integration Checklist (future, when ready to merge)

- [ ] Create `ws_audio_proto.c` / `.h` in `main/`
- [ ] Add stereo→mono downmix in send path
- [ ] Add 4-byte binary frame header
- [ ] Send `session_start` JSON on WS connect
- [ ] Parse `session_ack` and store server format
- [ ] Strip 4-byte header on receive before playing
- [ ] Handle DAC sample-rate switch on receive
- [ ] Add format selection to web dashboard (16k / 22k / 44k radio buttons)
- [ ] Update `app_nvs_save_audio()` to persist selected WS audio format
- [ ] Test with Python server above
- [ ] Git tag as v2.2.0