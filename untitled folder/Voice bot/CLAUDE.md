# Project Overview
**Voice Bot Pro** — an ESP32-S3 AI voice assistant running on a Waveshare ESP32-S3-Touch-AMOLED-1.75 (466×466 round AMOLED, touch). Built with ESP-IDF v5.5.2.
Hardware: ES7210 4-ch ADC (dual mic), ES8311 DAC + PA (GPIO 46), SD card via SDMMC 1-bit, 466×466 round AMOLED touch display.
# Architecture
## Initialization sequence (`main/main.c`)
`app_main()` initializes in order:
1. NVS → 2. Display (LVGL) → 3. SD card → 4. Audio codecs → 5. WiFi → 6. WebSocket client → 7. HTTP web server → 8. UI

The main loop runs every 5 s: reconnects WiFi if dropped, retries WebSocket with exponential backoff (5 s → 10 s → 20 s → 40 s → 80 s → 120 s ceiling), and logs heap stats every 30 s.
## Module map

| File                      | Responsibility                                                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `main/main.c`             | Init, callbacks, main loop                                                                                                                 |
| `main/app_nvs.c/h`        | NVS persistence — `app_settings_t` struct, namespace `"voicebot"`                                                                          |
| `main/app_audio.c/h`      | I2S capture (ES7210), PCM playback (ES8311), FFT spectrum, WAV record/playback to SD                                                       |
| `main/app_ws_client.c/h`  | WebSocket client (espressif/esp_websocket_client), text/binary/state callbacks, exponential backoff                                        |
| `main/app_webserver.c/h`  | HTTP dashboard on port 80, REST API (WiFi/WS/audio/SD/OTA/reboot), mDNS as `voicebot.local`                                                |
| `main/app_wifi.c/h`       | STA connect + AP fallback (192.168.4.1), mDNS                                                                                              |
| `main/app_ui.c/h`         | LVGL tileview — 3 swipeable screens, spectrum visualizer, AI bot UI                                                                        |
| `main/ws_audio_proto.c/h` | WebSocket audio framing — 4-byte binary header, stereo→mono downmix, JSON session handshake                                                |
| `main/qrcodegen.c/h`      | QR code generation (device info screen shows MAC address as QR)                                                                            |
| `components/bsp_extra/`   | Board-level codec init/control (`bsp_board_extra.h`): `bsp_extra_codec_init()`, `bsp_extra_codec_set_fs()`, `bsp_extra_codec_volume_set()` |
## UI Screens (`app_ui.h`)
Three screens on a horizontal tileview, swiped left/right:
- **Screen 0** (`UI_SCREEN_RECORDER`): Voice recorder with FFT spectrum, Record/Play/Stop
- **Screen 1** (`UI_SCREEN_AIBOT`): AI bot — Talk/Stop button (appears only when WS connected), AI response text
- **Screen 2** (`UI_SCREEN_DEVICE`): QR code of MAC address + readable MAC text
## WebSocket Audio Protocol (`ws_audio_proto.h`, `WS_AUDIO_PROTOCOL.md`)
On WS connect, device sends JSON `session_start`; server replies with `session_ack`. Binary frames carry a 4-byte header (`ws_audio_hdr_t`: type, flags, seq LE u16) followed by raw PCM-S16LE. Frame type `0x01` = mic→server, `0x02` = server→device. `WS_FLAG_LAST` (bit 0 of flags) marks the last frame of an utterance. The protocol layer downmixes I2S stereo to mono before sending.

Audio format is NVS-configurable: `ws_send_rate` (8000/16000/22050/44100 Hz) and `ws_send_channels` (1=mono recommended, 2=stereo).
## Settings (`app_nvs.h`)
All persistent config lives in `app_settings_t` (NVS namespace `"voicebot"`). Key fields: `wifi_ssid/pass/configured`, `ws_url/configured`, `speaker_volume`, `mic_gain`, `sample_rate`, `ws_send_rate`, `ws_send_channels`, `display_brightness`, `device_name`.

Use `app_nvs_get()` for read-only access. Call `app_nvs_save_*()` helpers or `app_nvs_save()` after mutating via `app_nvs_get_mutable()`.
## LVGL threading rule
All LVGL calls must be made under the display lock:
```c
bsp_display_lock(-1);
// ... LVGL operations ...
bsp_display_unlock();
```
Callbacks invoked from FreeRTOS tasks (audio capture, WebSocket events) must use this guard before touching any LVGL object.
## Partition layout

| Partition        | Size  |
| ---------------- | ----- |
| nvs              | 24 KB |
| factory (app)    | 8 MB  |
| storage (SPIFFS) | 7 MB  |
Total flash: 16 MB. Audio recordings go to SD card (`/sdcard/REC/`), not SPIFFS.
## Key config (sdkconfig.defaults)
- Target: `esp32s3`, 240 MHz, SPIRAM (Octal, 80 MHz)
- LVGL v9, FreeRTOS tick 1 kHz, `SPIRAM_MALLOC_ALWAYSINTERNAL=4096`
- Console UART baud: 2,000,000
- OTA over plain HTTP allowed (`ESP_HTTPS_OTA_ALLOW_HTTP=y`)
- mbedTLS: dynamic buffers, IN=16384 / OUT=2048 to conserve RAM