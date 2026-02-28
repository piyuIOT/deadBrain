# What Is This?
A standalone AI voice assistant running entirely on an ESP32-S3 microcontroller with a round 466×466 AMOLED touchscreen. You tap a button, speak, and your voice is streamed over WebSocket to a remote AI server. The server responds with text (displayed on screen) and optionally audio (played back through the built-in speaker). Everything — WiFi, display, audio capture and playback, configuration — runs on a single embedded chip.

The device ships with a built-in web dashboard (served at `voicebot.local`) where you can configure WiFi credentials, WebSocket server URL, audio format, volume, mic sensitivity, and more. A second screen doubles as a voice recorder with SD card storage. A third screen shows a QR code with the device's MAC address for identification.

**Hardware:** Waveshare ESP32-S3-Touch-AMOLED-1.75 (ESP32-S3, 8MB PSRAM, 16MB Flash, round display, ES7210 dual-mic ADC, ES8311 DAC/amp, SD card slot)
**Firmware:** ESP-IDF 5.4.0, FreeRTOS, LVGL 9.x
**Version:** v2.4.0

---
# File Table

| File                                                   | What It Does                                                                                                                                                          |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `main/main.c`                                          | App entry point — initializes all subsystems in order, wires up callbacks, runs the main reconnection loop                                                            |
| `main/app_nvs.h/c`                                     | Persistent settings storage using ESP32 NVS flash — saves and loads WiFi, audio, and WebSocket config across reboots                                                  |
| `main/app_wifi.h/c`                                    | WiFi management — connects in STA mode, falls back to SoftAP for initial setup, advertises device on the network via mDNS                                             |
| `main/app_audio.h/c`                                   | Core audio engine — handles I2S mic capture, FFT spectrum analysis, WAV file recording and playback via the DAC                                                       |
| `main/app_ws_client.h/c`                               | WebSocket client — connects to the AI server, manages reconnection with exponential backoff, reassembles fragmented messages                                          |
| `main/ws_audio_proto.h/c`                              | Audio protocol layer — frames raw PCM into binary WebSocket packets, handles stereo-to-mono downmix, and negotiates audio format with the server via a JSON handshake |
| `main/app_webserver.h/c`                               | HTTP web server — serves the configuration dashboard and a REST API for WiFi, audio, WebSocket settings, SD file management, and OTA updates                          |
| `main/app_ui.h/c`                                      | LVGL touch UI — implements three screens: the AI voice bot screen with live spectrum rings, a voice recorder, and a device info/QR code screen                        |
| `main/app_nvs.h/c`                                     | NVS header — defines the settings struct and public API for the persistence module                                                                                    |
| `main/qrcodegen.h/c`                                   | Standalone QR code generator — encodes the device MAC address into a bitmap for LVGL to render on the device info screen                                              |
| `components/bsp_extra/`<br>`src/bsp_board_extra.c`     | Hardware abstraction for the audio codecs — wraps the ES7210 ADC and ES8311 DAC so the app doesn't touch hardware registers directly                                  |
| `components/bsp_extra/`<br>`include/bsp_board_extra.h` | Public API for the BSP — exposes codec init, sample rate switching, volume, mute, and raw I2S read/write                                                              |
| `partitions.csv`                                       | Flash partition map — defines NVS, PHY calibration, factory app, and SPIFFS storage regions                                                                           |
| `sdkconfig` / `sdkconfig.defaults`                     | ESP-IDF build configuration — CPU speed, PSRAM mode, LVGL settings, WiFi, WebSocket, mbedTLS tuning                                                                   |
| `main/idf_component.yml`                               | Component dependency manifest — declares LVGL, esp-dsp, websocket client, mDNS, audio player, and display BSP versions                                                |
| `CMakeLists.txt`                                       | Top-level CMake project definition                                                                                                                                    |
| `main/CMakeLists.txt`                                  | Source file list and component registration for the main application                                                                                                  |
| `WS_AUDIO_PROTOCOL.md`                                 | Protocol documentation — explains the binary frame format, JSON session handshake, bandwidth tradeoffs, and design rationale                                          |
| `.vscode/tasks.json`                                   | VS Code build tasks — automates build, flash, and monitor commands for the connected device                                                                           |

---
# Design Choices & Architecture Notes
## 1. Binary WebSocket Protocol with JSON Handshake
Rather than sending raw PCM or encoding audio into Base64 JSON, the protocol uses a custom 4-byte binary frame header (`type | flags | uint16 sequence`) prepended to raw PCM. This is intentional:

- **Overhead:** 4 bytes per frame vs. ~33% size increase with Base64 or JSON wrapping
- **Ordering:** Sequence numbers let the server detect dropped/reordered frames without TCP-level inspection
- **Negotiation:** A one-time JSON `session_start` / `session_ack` handshake lets the server know the audio format (sample rate, channels) at connect time rather than assuming it. If the user changes audio settings and reconnects, the server sees fresh metadata.

The protocol is documented in `WS_AUDIO_PROTOCOL.md` — an unusual move for embedded firmware, suggesting the author anticipated multiple server implementations needing to interop.
## 2. Stereo Capture, Mono Transmission
The ES7210 ADC always captures stereo (two physical mics). Rather than re-engineering the capture path, the protocol layer performs a L+R channel average before transmission. This halves the bandwidth (32 KB/s vs. 64 KB/s at 16kHz) with minimal voice quality impact for speech AI. The mono/stereo choice is configurable per-session via NVS and negotiated in the handshake.
## 3. Layered Audio Architecture
```
app_audio   → handles I2S, FFT, WAV, callbacks
ws_audio_proto → handles framing, downmix, sequence
app_ws_client  → handles TCP/WebSocket lifecycle
```

Each layer is independently swappable. You could replace the WebSocket client with an HTTP chunked upload or MQTT without touching the audio DSP layer.
## 4. Callback-Driven Data Flow (No Shared Queues)
Audio data flows through callbacks rather than FreeRTOS queues: `app_audio` calls `on_audio_data()` which calls `app_ws_send_audio()`. This avoids copy overhead and queue latency for real-time audio. The tradeoff is tighter coupling between timing domains — the callback runs inside the capture task's context, so any slow operation in the chain blocks the next audio frame.
## 5. Exponential Backoff on Two Levels
Both WiFi and WebSocket reconnection use exponential backoff independently:
- WiFi: Max 5 retries before switching to AP mode
- WebSocket: 5s → 10s → 20s → 40s → 80s → 120s cap, resets on clean connect

This means if the AI server goes down, the device quietly backs off to 2-minute retries rather than hammering it. The main loop checks both states every 5 seconds and chains them (WiFi must be up before attempting WS reconnect).
## 6. Embedded Web Dashboard (No File System Required)
The entire ~1000-line HTML/CSS/JS dashboard is stored as a C string literal inside `app_webserver.c`. No SPIFFS or SD card needed to serve the configuration UI. This is common in small IoT devices but means updating the dashboard requires a firmware flash. The REST API endpoints are all JSON and could be driven by any external client.
## 7. LVGL on a Round Display
The 466×466 round display is circular, so rectangular LVGL widgets would draw into the invisible corners. The spectrum visualization is radial (64 bars arranged in a circle) specifically to fit the round form factor. Standard LVGL containers are used for the other two screens but kept centered to avoid corner artifacts.
## 8. FFT Pipeline Details
- **Window:** Hann window applied before FFT to reduce spectral leakage from the 200ms frame edges
- **Size:** 256-point FFT → 128 usable frequency bins (Nyquist)
- **Scale:** Converted to dB, clamped between -60 dB (noise floor) and -6 dB (near-peak), then linearly normalized to 0.0–1.0 for the UI
- **Update Rate:** 50ms spectrum update task (20 FPS) is independent of the 200ms audio capture cycle — the UI refreshes 4× per audio frame using the latest spectrum snapshot protected by a mutex
## 9. NVS as Single Source of Truth
All runtime-configurable state lives in NVS. On boot, every subsystem reads from the single `app_settings_t` struct loaded by `app_nvs_init()`. The web dashboard only writes to NVS; it never directly calls into audio or WiFi APIs. A reboot applies the new settings cleanly. The exception is volume and sample rate changes, which are applied immediately at the codec level without requiring reboot.
## 10. Battery Optimization (Active Branch)
The current branch `feat/battery-optimization` indicates active work on power management. The current firmware runs the CPU at 240MHz continuously with no light-sleep or modem-sleep between audio frames. The 50ms spectrum task and 5s main loop polling are the most obvious power reduction targets — the architecture supports adding sleep gates cleanly since the callback model already separates "data arriving" from "CPU busy."

---
# Quick Reference

| Component | Technology | Key Config |
|-----------|-----------|------------|
| MCU | ESP32-S3, 240MHz | Dual core, one pinned to audio |
| Display | 466×466 AMOLED | LVGL 9.x, 15ms refresh |
| Audio In | ES7210 ADC | 16kHz default, 16-bit stereo → mono |
| Audio Out | ES8311 DAC | Same sample rate, amplifier on GPIO46 |
| WiFi | STA + SoftAP fallback | mDNS: voicebot.local |
| AI Transport | WebSocket (WS/WSS) | Custom binary+JSON protocol |
| Settings | NVS Flash | 24KB partition |
| Storage | SD card (SDMMC) | WAV recordings in /sdcard/REC/ |
| Web UI | Vanilla JS + CSS | Port 80, dark theme |
| Build | ESP-IDF 5.4.0 + CMake | idf.py build flash monitor |
