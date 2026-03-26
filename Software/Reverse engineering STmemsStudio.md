For custom ST eval kit pipelines, if you want to bypass the memsStudio, the simplest thing to do is:
Run a wireshark USB sniffer and connect your eval kit and do the task on mems studio as usual, then stop the recording and share this with claude to reverse engineer the USB communication.
> This USB sniffer will work on windows or linux but not on mac (those expensive shit got some issue in giving devs enough power)

---

## STEVAL-MKI109D + STEVAL-MKI237KA (LSM6DSV16BX) — Reverse Engineered Protocol

Hardware: STEVAL-MKI109D USB bridge (ProfiMT+H5 board, firmware V2.6.17) with STEVAL-MKI237KA daughter board (LSM6DSV16BX accelerometer).

### Transport

USB CDC virtual COM port — 115200 baud, 8N1. All commands are ASCII, all data is binary.

### Command format

Every host→device command is framed as:

```
*<command>\r\n
```

Replies come back as a single line terminated with `\r\n`. Register read replies use the form `RXXhYYh` (address, value, both in hex).

### Key commands

| Command | Description |
|---|---|
| `*dbreset` | Reset the daughter board |
| `*board` | Returns board name string (e.g. `ProfiMT+H5`) |
| `*ver` | Returns firmware version string (e.g. `V2.6.17`) |
| `*time_set HH MM SS` | Set RTC time |
| `*date_set DD MM YY` | Set RTC date |
| `*setdb237ka` | Select MKI237KA daughter board |
| `*tim7` | Enable Timer 7 (required before register access) |
| `*dat2` | Set data format mode 2 |
| `*zoff` | Apply Z-axis offset calibration |
| `*rXX` | Read register at hex address XX — reply: `RXXhYYh` |
| `*wXXYY` | Write value YY (hex) to register XX (hex) |
| `*wclkNNNN` | Set TDM clock in Hz (e.g. `*wclk16000`) |
| `*start_data` | Arm data streaming (registers latched) |
| `*start` | Begin streaming data frames over USB |
| `*stop` | Stop streaming |

### TDM 16 kHz ±2g configuration sequence

After selecting the daughter board, write these registers in order:

| Register | Address | Value | Notes |
|---|---|---|---|
| CTRL1 | `0x10` | `0x20` | Accel on, ODR, FS = ±2g |
| CTRL2 | `0x11` | `0x00` | Gyro off |
| CTRL7 | `0x16` | `0x00` | |
| TDM_CFG0 | `0x6C` | `0xE3` | |
| TDM_CFG1 | `0x6D` | `0xF0` | |
| TDM_CFG2 | `0x6E` | `0x00` | |

Then send `*wclk16000`, `*start_data`, `*start`.

Verify with `*r10` — should reply `R10h20h`.

### Streaming frame format

Each sample is a 15-byte frame:

```
[74 64] [Xhi Xlo] [Yhi Ylo] [Zhi Zlo] [54] [ts0 ts1 ts2 ts3] [0D 0A]
  "td"   X int16BE  Y int16BE  Z int16BE  "T"  timestamp uint32LE µs  CRLF
```

- Sync: `0x74 0x64` (`"td"`) — 2 bytes
- X, Y, Z: signed int16, **big-endian** (MSB first, TDM bus order) — 6 bytes
- Tag: `0x54` (`"T"`) — 1 byte
- Timestamp: unsigned uint32, **little-endian**, microseconds — 4 bytes
- Terminator: `\r\n` — 2 bytes

**Total: 15 bytes per sample.**

### Sensitivity

±2g mode: **0.061 mg per LSB** (from LSM6DSV16BX datasheet).

Convert raw counts to mg: `value_mg = raw_int16 * 0.061`

Gravity sanity check: at rest, `sqrt(X² + Y² + Z²)` ≈ 1000 mg (1g ≈ 991 mg observed).

### Initialization sequence (full)

```
*dbreset
*board          → ProfiMT+H5
*ver            → V2.6.17
*time_set HH MM SS
*date_set DD MM YY
*setdb237ka
*ver            (flush reply after board re-enumerate)
*dbreset
*setdb237ka
*tim7
*dat2
*zoff
--- configure registers ---
*stop
*tim7
*w1020  *w1100  *w1600  *w6CE3  *w6DF0  *w6E00
*wclk16000
*start_data
--- verify ---
*r10            → R10h20h
--- stream ---
*start
... 15-byte frames ...
*stop
```

### Notes

- `cu.usbmodem*` and `tty.usbmodem*` both appear on macOS — use `cu.*` (avoids DCD/DTR handshake issues).
- A small sleep (~10 ms) between register writes is needed for reliable enumeration.
- The board re-enumerates after `*setdb237ka`, so a second `*dbreset` + `*setdb237ka` is needed before writing sensor registers.
- Stream sync is robust: scan incoming bytes for `0x74 0x64`, then validate the full 15-byte frame before trusting axis data.
