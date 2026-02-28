# Testing
To test code changes: use `./build.sh --help` and then respective commands for cleanbuild, flash, monitor
# Project scope
ESP-IDF v5.x C project targeting **ESP32-P4 function ev board** and **ESP32-S3 korvo2, and ESP32-S3 waveshare amoled 175 board** (conditionally compiled board specific). 
- Records audio
- Processes audio through ESP-AFE
- Saves processed and raw WAV files to SD
- Web streaming (#TODO)
- Amoled display UI (#ONGOING)
# Board Context Resources (`context/`)
Per-board reference material lives in `context/`. 
- Wiki links
- Other resources
- Basic pinout
# Reference repos (`context/example_repos/`)
Always take context or reference from here first, then go online or use your memory.
Always read the vendor example for the relevant feature before implementing — driver init order, Kconfig deps, and pin assignments are all there.

| Repo                   | Location                                                                           | Source                                                      | Relevant for                                                  |
| ---------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------- |
| `waveshare-amoled-175` | `context/example_repos/waveshare-amoled-175/examples/ESP-IDF-v5.5/`                | https://github.com/waveshareteam/ESP32-S3-Touch-AMOLED-1.75 | Waveshare board                                               |
| `esp-dev-kits`         | `context/example_repos/esp-dev-kits/examples/esp32-p4-function-ev-board/examples/` | https://github.com/espressif/esp-dev-kits                   | Different dev boards including ESP32-P4 Function EV Board     |
| `esp-adf`              | `context/example_repos/esp-adf/examples/`                                          | https://github.com/espressif/esp-adf                        | Various audio processing including ESP32-S3-Korvo-2 board use |
| `esp-skainet`          | `context/example_repos/esp-skainet/examples/`                                      | https://github.com/espressif/esp-skainet                    | All boards: wake word, speech commands, noise suppression     |
# Project Layout

| File                                      | Usage                                                                             |
| ----------------------------------------- | --------------------------------------------------------------------------------- |
| `main/main.c`                             | Entry point. Hardware init, conditionally compiled, orchestrator of all tasks     |
| `main/pins.h`                             | Pin defines for all boards                                                        |
| `main/config.h` and `main/config.c`       | Reads config files from SD card to configure ADC, DAC, AFE, recorder, etc.        |
| `main/recording.h` and `main/recording.c` | Feed and fetch AFE tasks, WAV header write                                        |
| `main/playback.h` and `main/playback.c`   | Plays back latest recording. Standalone and UI-mode variants                      |
| `main/ui_app.h` and `main/ui_app.c`       | (Waveshare only) AMOLED UI app. Record, play, file list.                          |
| `libraries/display_ui/`                   | LVGL widget library for the AMOLED display                                        |
| `libraries/ES8311/`                       | ES8311 DAC/ADC codec driver. Recording (P4) + playback (all boards)               |
| `libraries/ES7210/`                       | ES7210 ADC codec driver. S3 recording only                                        |
| `libraries/format_wav/`                   | Header-only WAV struct and PCM header macro                                       |
| `libraries/sdCard/`                       | SD mount/unmount and file number scanner. Per-board source selected at build time |
| `partitions.csv`                          | 3MB app + 4MB SPIFFS model partition. Both targets                                |
| `sdkconfig.defaults`                      | Common Kconfig: FATFS, flash, PSRAM, NSNet2, esp-sr                               |
| `sdkconfig.defaults.esp32p4`              | P4: HEX PSRAM 200MHz                                                              |
| `sdkconfig.defaults.esp32p4.function_ev`  | Selects P4 Function EV board                                                      |
| `sdkconfig.defaults.esp32s3`              | S3: OCT PSRAM 80MHz                                                               |
| `sdkconfig.defaults.esp32s3.waveshare`    | Selects Waveshare AMOLED board                                                    |
| `sdkconfig.defaults.esp32s3.korvo2`       | Selects Korvo-2 board                                                             |
| `example config/RECORDING.cfg`            | `record_time`, `record_raw`. All boards                                           |
| `example config/ESP_AFE.cfg`              | `afe_topology`, `ns_mode`, `agc_*`. All boards                                    |
| `example config/ES8311_DAC.cfg`           | `voice_volume`. All boards                                                        |
| `example config/ES8311_ADC.cfg`           | ES8311 ADC/DSP params. P4 only                                                    |
| `example config/ES7210.cfg`               | ES7210 mic params. S3 boards                                                      |
| `context/example_repos/`                  | Reference codebase from vendors                                                   |
# Component Dependencies
`main`: `sdCard`, `ES8311` (all), `ES7210` (S3 recording), `format_wav`, `esp_driver_i2s`, `esp_driver_i2c`, `esp_driver_gpio`, `esp-sr`

Waveshare S3 also: `display_ui`, `esp32_s3_touch_amoled_1_75` (BSP managed component).

S3: ES7210 (ADC/recording) + ES8311 (DAC/playback) share I2S+I2C, never active simultaneously.

- `display_ui`: `lvgl` (via BSP), `sdCard`, `esp_log`
- `ES8311` / `ES7210`: `esp_driver_i2c`, `esp_driver_i2s` (public); `esp_codec_dev` (private)
- `sdCard` P4: `fatfs`, `esp_driver_sdmmc`, `sdmmc`, `vfs`
- `sdCard` Waveshare S3: `fatfs`, `spi_flash`, `esp_driver_spi`, `sdmmc`, `vfs`
- `sdCard` Korvo-2: `fatfs`, `esp_driver_sdmmc`, `sdmmc`, `vfs`
- `format_wav`: none (header-only)
- `esp-sr`: ESP-AFE, NSNet2, WebRTC AGC. Kconfig in `sdkconfig.defaults`.

New components: `libraries/` — auto-discovered via `EXTRA_COMPONENT_DIRS`.
# Git Workflow
- Do not fast forward merge.
- Follow industry standard branch naming conventions, commit message conventions, and any other conventions followed.
# Conventions
- **C99**, no C++. All headers use `extern "C"` guards for compatibility.
- Error handling: `ESP_ERROR_CHECK()` for fatal errors, `ESP_RETURN_ON_ERROR()` inside library functions.
- Logging: `ESP_LOGI/W/E()` with a static `TAG` per file.
- WAV filenames: `RECnnnnn.WAV` (processed, always) and `RAWnnnnn.WAV` (raw, optional). 5-digit zero-padded, max 99999, wraps to 1, cyclic rewriting.
# Multi-Target Conditional Compilation
**Chip-family guards** (`CONFIG_IDF_TARGET_ESP32P4` / `ESP32S3`) in `main/main.c`:
- Codec includes: P4 → `es8311.h`; S3 → `es7210.h` + `es8311.h`
- `codec_config_t` typedef + `CODEC_CONFIG_DEFAULT()` macro
- P4-only config: HPF, ALC, automute, EQ, ADC oversampling, `adc_volume`, `cfg.voice_volume`
- Codec init/deinit: `es8311_init(i2c_bus, NULL, rx_handle, &cfg)` vs `es7210_init(i2c_bus, rx_handle, &cfg)`

**Board-level guards** (`CONFIG_BOARD_ESP32P4_FUNCTION_EV` / `BOARD_WAVESHARE_S3_AMOLED_175` / `BOARD_KORVO2`):
- All pin definitions, per-board defaults (Korvo-2: `mic_gain=36`), banner text

`main/CMakeLists.txt`: `CODEC_LIBS` = `ES8311` (P4) or `ES7210;ES8311` (S3).

`sdCard/CMakeLists.txt`: selects source by `CONFIG_BOARD_*`. Unknown board → `FATAL_ERROR`.

## ESP-AFE Integration

### Two-Task Architecture

```
[Feed Task - core 0]                [Fetch Task - core 1]
  I2S read (feed_chunksize)            afe_handle->fetch()
  → write to RAW file (if enabled)     → write result->data to REC file
  → afe_handle->feed()                 → track rec_bytes_written
  → repeat until total_data_size       → wait for BIT_FEED_DONE
  → set stop_flag, signal FEED_DONE    → drain remaining with fetch_with_delay()
                                        → signal FETCH_DONE
                                     [app_main waits for FEED_DONE + FETCH_DONE]
                                        → WAV header fixup (seek + rewrite)
```

- Feed: core 0, 8192B stack. NSNet2 inference inside `feed()` needs ~6KB.
- Fetch: core 1, 8192B stack. **Must be core 1** — `record_raw=1` means both tasks write SD; FAT32 single mutex stalls fetch if same core → dropped audio.
- Coordination: `EventGroupHandle_t`, `BIT_FEED_DONE` + `BIT_FETCH_DONE`.
- Shared state: `recording_ctx_t` (stack in `app_main`, pointer passed to both tasks).

### AFE Configuration

```c
afe_config_init("M", models, AFE_TYPE_VC, AFE_MODE_HIGH_PERF);
// "M" = single mic, AFE_TYPE_VC = voice comms
// Disabled: aec, se, vad, wakenet
// Enabled: ns (NSNet2), agc (WebRTC)
// Memory: AFE_MEMORY_ALLOC_MORE_PSRAM
```

NSNet2 requires `CONFIG_SR_NSN_NSNET2=y`. Without it, falls back to WebRTC NS.

### AFE Requirements

16kHz / 16-bit / mono. Enforced in `app_main` after config parse (overrides with `ESP_LOGW`).

### Dual WAV Output

- REC: placeholder header (`data_size=0`), fixup after recording with actual `rec_bytes_written`.
- RAW: pre-calculated header, no fixup.
- Both get same number: `sdcard_check_highest_file_number(SDCARD_SCAN_BOTH) + 1`.

### Graceful Fallback

AFE init failure → `raw_fallback:` → single-loop raw recording → `RAWnnnnn.WAV` only.

### Key esp-sr Kconfig Settings

```
CONFIG_SR_NSN_NSNET2=y     # NSNet2 (default WebRTC is much worse)
CONFIG_SR_MN_NONE=y        # No MultiNet
CONFIG_SR_WN_NONE=y        # No WakeNet
```

### Partition Table

16MB flash: `factory` 3MB app + `model` 4MB SPIFFS (NSNet2, loaded via `esp_srmodel_init("model")`).

### PSRAM

AFE needs ~824KB PSRAM.
```
# common
CONFIG_SPIRAM=y
CONFIG_SPIRAM_USE_CAPS_ALLOC=y
# P4
CONFIG_SPIRAM_MODE_HEX=y
CONFIG_SPIRAM_SPEED_200M=y
# S3
CONFIG_SPIRAM_MODE_OCT=y
CONFIG_SPIRAM_SPEED_80M=y
CONFIG_SPIRAM_FETCH_INSTRUCTIONS=y
CONFIG_SPIRAM_RODATA=y
```

## ES8311 Driver Pattern

Two layers:
1. `esp_codec_dev`: init, sample config, gain.
2. Direct I2C register writes (`es8311_write_reg`): HPF, ALC, automute, EQ, ADC OSR/scale, fade. ADC mode only.

`es8311_init()` derives mode from non-NULL handles:
- `tx_handle` only → DAC
- `rx_handle` only → ADC
- both → full duplex

Gain: `esp_codec_dev_set_out_vol()` (DAC) or `esp_codec_dev_set_in_gain()` (ADC). `es8311_apply_advanced_config()` skipped in DAC-only mode.

**Naming:** typedef is `esp_codec_dec_work_mode_t` (with `dec`), enum values are `ESP_CODEC_DEV_WORK_MODE_*`.

Order: `esp_codec_dev` init first → register writes via `s_ctrl_if`. No separate `i2c_master_bus_add_device()` — `audio_codec_new_i2c_ctrl()` adds it.

I2S must be `i2s_channel_init_std_mode()` before `es8311_init()`. Causes `dma frame num adjusted` warnings — expected.

Register writes: read-modify-write. EQ: 30-bit Q1.29, 4 registers each, via `es8311_write_eq_coeff()`. P4 only.

## ES7210 Driver Pattern (S3 only)

Two layers:
1. `esp_codec_dev`: init, sample config, mic gain.
2. Direct I2C write: ADC power-up register 0x06.

Order: `esp_codec_dev` init → register writes via `s_ctrl_if`.

I2S must be initialized before `es7210_init()`. `dma frame num adjusted` warnings expected.

ES7210 outputs stereo (MIC1=left, MIC2=right). Call `esp_codec_dev_open()` with **`channel=1`** → MONO, captures MIC1 only. `channel=2` → STEREO interleave, halves effective sample rate, AFE discards as noise.

## ES8311 Driver Pattern — Playback (all boards)

`es8311_init(i2c_bus, tx_handle, NULL, &cfg)` — TX-only (DAC). I2S: `i2s_new_channel(&cfg, &tx_handle, NULL)`. `PIN_I2S_DOUT` → ES8311 DIN; `din = I2S_GPIO_UNUSED`.

## Playback

`play_rec_file()` — self-contained, called automatically after recording.

### Flow

```
play_rec_file()
  1s vTaskDelay          ← settle after recording teardown
  i2c_new_master_bus()   ← fresh I2C (recording deleted the bus)
  sdcard_mount()
  sdcard_check_highest_file_number(SDCARD_SCAN_REC)
  fopen RECnnnnn.WAV, read + validate wav_header_t
  i2s_new_channel() TX only
  i2s_channel_init_std_mode() + enable
  es8311_init(i2c_bus, tx_handle, NULL, &pb_cfg)
  gpio_set_level(PIN_PA_EN, 1)
  fread → i2s_channel_write loop (4KB chunks)
  fclose → es8311_deinit → I2S delete → PA off → SD unmount → i2c_del_master_bus
```

### Isolation

Recording `cleanup:`: deinits codec, deletes I2S RX, PA off, SD unmount, **deletes I2C bus**.
`play_rec_file()`: fresh I2C, mount SD, ES8311 TX-only, stream, full teardown. Neither borrows from the other.

### WAV header read

Reads `sizeof(wav_header_t)` for format. Configures I2S + ES8311 from file header. Guards `data_chunk.subchunk_size == 0` (power loss during recording).

## Waveshare AMOLED UI

`CONFIG_BOARD_WAVESHARE_S3_AMOLED_175=y` only. Entry: `ui_app_run()`, replaces the bare recording loop.

### BSP integration

BSP (`waveshare__esp32_s3_touch_amoled_1_75`): CO5300 display (SPI2, 466×466 RGB565), CST9217 touch (I2C), LVGL v9 task.

| Call | Purpose |
|------|---------|
| `bsp_i2c_init()` | Shared I2C bus (SCL=14, SDA=15) |
| `bsp_i2c_get_handle()` | Bus handle for codec |
| `bsp_display_start()` | Init SPI2, display, touch, LVGL task |
| `bsp_display_backlight_on()` | Backlight via AXP2101 |
| `bsp_display_lock(portMAX_DELAY)` | Acquire LVGL mutex |
| `bsp_display_unlock()` | Release LVGL mutex |

LVGL task: priority 6. `app_main`: priority 1. LVGL preempts after every unlock.

### Three-phase LVGL init pattern

SD I/O inside `bsp_display_lock()` starves the render task → display stays black.

```c
/* Phase A — build skeleton UI (no I/O) */
bsp_display_lock(portMAX_DELAY);
ui_init(evq);
ui_set_status("Loading files...");
bsp_display_unlock();
/* LVGL preempts here, renders frame */

/* Phase B — SD scan outside lock */
ui_scan_files();

/* Phase C — populate inside lock (fast, cache built) */
bsp_display_lock(portMAX_DELAY);
ui_populate_file_list();
ui_set_status("Ready");
bsp_display_unlock();
```

`ui_refresh_file_list()` = B+C. OK post-recording (small file count).

### display_ui layout (466×466)

| Widget | Position | Notes |
|--------|----------|-------|
| Title "Voice Recorder" | y=10, full width | Montserrat 24 |
| Status label | y=46, full width | Montserrat 18, dimmed grey |
| RECORD button | y=80, h=90 | Red / dark red when active |
| PLAY LATEST button | y=182, h=70 | Green / dark green when active |
| "SD Card Recordings" header | y=264 | Montserrat 18 |
| Scrollable file list | y=292, to bottom | `lv_list` with play buttons |

Background `0x0D1B2A`. Never pure black — indistinguishable from powered-off on AMOLED.

### Touch diagnostic

```c
lv_indev_t *indev = lv_indev_get_next(NULL);
while (indev) {
    if (lv_indev_get_type(indev) == LV_INDEV_TYPE_POINTER) {
        lv_indev_add_event_cb(indev, touch_log_cb, LV_EVENT_PRESSED, NULL);
        break;
    }
    indev = lv_indev_get_next(indev);
}
```

`touch_log_cb` calls `lv_indev_get_point()` + logs x/y.

### Known issue: display stays black

LVGL renders, touch works, callbacks fire — no pixels on CO5300. Flush callback does RGB565 byte-swap + `esp_lcd_panel_draw_bitmap()`. CO5300 logs `W: The 3Ah command has been used and will be overwritten` — COLMOD register overwritten during init. **Active investigation point.**

## Config System

`key=value` files on SD root. All optional. `#` comments, `0x` hex. Unknown keys: `ESP_LOGW` + skip.

| File | Boards | Keys |
|------|--------|------|
| `RECORDING.cfg` | all | `record_time`, `record_raw` |
| `ESP_AFE.cfg` | all | `afe_topology`, `ns_mode`, `agc_enable`, `agc_target_level`, `agc_max_gain` |
| `ES8311_DAC.cfg` | all | `voice_volume` |
| `ES8311_ADC.cfg` | P4 only | `sample_rate`, `bit_depth`, `channels`, `mic_gain`, `adc_volume`, `hpf_enable`, `hpf_coeff_stage1`, `hpf_coeff_stage2`, `adc_osr`, `adc_double_speed`, `adc_scale`, `alc_enable`, `alc_window`, `alc_max_level`, `alc_min_level`, `automute_enable`, `automute_window`, `automute_threshold`, `adc_ramp_rate`, `adc_ram_clear`, `eq_enable`, `eq_b0`–`eq_a2` |
| `ES7210.cfg` | S3 only | `sample_rate`, `bit_depth`, `channels`, `mic_gain` |

Load order: `RECORDING.cfg` → `ESP_AFE.cfg` → `ES8311_DAC.cfg` → `ES8311_ADC.cfg` / `ES7210.cfg`.

- `ns_mode`: `net` (NSNet2) or `webrtc`. `net` requires `CONFIG_SR_NSN_NSNET2=y` at build time.
- `voice_volume` (0–100, default 70): DAC level all boards. P4 also sets `cfg.voice_volume` for recording codec.
- `AUDIO.CFG` no longer read.

To add a config key:
1. Codec param → field in config struct + `_CONFIG_DEFAULT()` macro
2. App param → `static` var in `config.c`
3. `else if` in handler (`handle_recording_key`, `handle_afe_key`, `handle_es8311_dac_key`, `handle_es8311_adc_key`, `handle_es7210_key`)
4. Document in `example/` config file

## Hardware Pin Map

Authoritative pinouts in `context/`. Quick reference:

| Signal | P4 GPIO | Waveshare S3 GPIO | Korvo-2 S3 GPIO |
|--------|---------|-------------------|-----------------|
| I2S MCLK | 13 | 42 | 16 |
| I2S BCLK | 12 | 9 | 9 |
| I2S WS | 10 | 45 | 45 |
| I2S DOUT | 9 | 8 | 8 |
| I2S DIN | 11 | 10 | 10 |
| I2C SDA | 7 | 15 | 17 |
| I2C SCL | 8 | 14 | 18 |
| PA Enable | 53 | 46 | 48 |
| SD (SDMMC CLK/CMD/D0-D3) | 43,44,39-42 | — | — |
| SD SPI (MOSI/SCK/MISO/CS) | — | 1,2,3,41 | — |
| SD (SDMMC 1-bit CLK/CMD/D0) | — | — | 15,7,4 |

## Common Pitfalls

- **Target/board switching:** `rm sdkconfig` when switching. Stale `CONFIG_BOARD_*` persists otherwise.
- **CMake REQUIRES — use `SDKCONFIG_DEFAULTS` not `CONFIG_BOARD_*`:** Kconfig vars unavailable at component-collection time. Use `if(SDKCONFIG_DEFAULTS MATCHES "waveshare")`. Use semicolons in cmake lists: `set(UI_LIBS "a;b")`, not spaces.
- **Korvo-2 vs Waveshare S3:** Both `esp32s3`. Board via `CONFIG_BOARD_KORVO2` / `CONFIG_BOARD_WAVESHARE_S3_AMOLED_175`.
- **`sdkconfig.defaults.*`:** Only applied when key absent from `sdkconfig`. `rm sdkconfig` to re-apply.
- **I2C address 8-bit format:** ES8311 = `0x18 << 1 = 0x30`; ES7210 = `0x40 << 1 = 0x80`. Driver shifts right internally.
- **ES7210 `channel=1`:** `esp_codec_dev_open()` must use `channel=1` (MONO). `channel=2` → STEREO DMA, half effective sample rate, AFE discards.
- **ES8311 ADC is mono.** `channels=2` won't produce real stereo.
- **MCLK:** Must be 256× for 16-bit. AFE always forces 16-bit.
- **EQ (P4):** Active requires MCLK/LRCK >= 256. Bypassed >= 240.
- **ADC OSR (P4):** >= 15 (single speed), >= 16 (double speed). <= 14 invalid.
- **SD P4:** Internal LDO channel 4 for IO power.
- **SD S3:** `esp_vfs_fat_sdspi_mount()`, no LDO.
- **`format_wav`:** Header-only. CMakeLists only registers `INCLUDE_DIRS`, no `SRCS`.
- **Feed task stack >= 8192.** NSNet2 needs ~6KB. 4096 → stack overflow.
- **`sdkconfig` caching:** `rm sdkconfig` to pick up Kconfig changes.
- **File number scanning:** Recording: `SDCARD_SCAN_BOTH`. Playback: `SDCARD_SCAN_REC`.
- **REC WAV header fixup:** Written `data_size=0`, fixup via `fseek` after recording. Power loss → invalid header, data intact.
- **AFE fetch drain:** After feed done, drain with `fetch_with_delay()` until NULL. Otherwise last ~hundreds ms of audio lost.
- **ES7210 stereo clobber:** `channel=2` → STEREO DMA. Fix: `channel=1` in `es7210.c`. Don't try restoring slot mode after init.
- **`record_raw=1` FATFS contention:** Feed (core 0) + fetch (core 1) write SD simultaneously. Same core → FAT32 mutex stalls fetch → `Ringbuffer of AFE(FEED) is full`, dropped audio (~2.2s/10s). Fetch must be core 1.
- **`idf_component.yml`:** Must exist before first build. Declares `esp_codec_dev`, `esp-sr`. Identical for both targets.
- **Waveshare S3 I2C:** SCL=GPIO14, SDA=GPIO15. Context README has them swapped — wrong. Reversed pins → all I2C fails silently.
- **`esp_codec_dev_delete` leaks ctrl_if/data_if:** Call `audio_codec_delete_ctrl_if(s_ctrl_if)` + `audio_codec_delete_data_if(s_data_if)` after `esp_codec_dev_delete()`. Otherwise `i2c_del_master_bus` fails ("devices still attached").
- **`i2s_channel_disable` after `es8311_deinit()`:** Don't. `esp_codec_dev_close()` already disables. Call only `i2s_del_channel()`.
- **`ns_mode=net`:** Requires `CONFIG_SR_NSN_NSNET2=y` at build time. Missing → silent WebRTC fallback. Missing model partition → `raw_fallback`.
- **`AUDIO.CFG` ignored.** Firmware reads five separate files. `AUDIO.CFG` on SD has no effect.
- **AXP2101 BLDO2 (MIC VDD):** On by default via OTP. No init needed.
- **AMOLED pure black = off.** Use `0x0D1B2A` minimum.
- **SD I/O inside `bsp_display_lock()`:** Starves LVGL render task. Use three-phase init.
- **`play_rec_file()` vs `play_file_with_bus()`:** `play_rec_file()` = standalone (own I2C+SD lifecycle). `play_file_with_bus()` = UI mode (SD+I2C already up, only I2S+codec created/destroyed).
- **CMake REQUIRES for `display_ui`:** `if(SDKCONFIG_DEFAULTS MATCHES "waveshare")`. Semicolons in cmake list: `set(UI_LIBS "display_ui;esp32_s3_touch_amoled_1_75")`.
