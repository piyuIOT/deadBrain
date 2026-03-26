#!/usr/bin/env python3
import os, re

VAULT = os.path.dirname(os.path.abspath(__file__))

TASKS = {
    "2026/02/02": "Filling HR documentation",
    "2026/02/03": "Setting up developer environment for ESP-IDF",
    "2026/02/04": "ESP32P4 basic coding",
    "2026/02/05": "ESP32P4 mic, microSD working",
    "2026/02/06": "Sick Leave",
    "2026/02/09": "ES32P4 ES3811 Codec config working",
    "2026/02/10": "ESP AFE working",
    "2026/02/11": "Laptop crashed, OS reinstall, Setup, autoBackup!",
    "2026/02/12": "Find board for Voice assistant, review schematic",
    "2026/02/13": "Schematic review of voice assistant board, and preliminary coding",
    "2026/02/16": "ESP32S3 (Korvo 2 and Waveshare Amoled 175) Mic and microSD working",
    "2026/02/17": "ESP32S3 Waveshare amoled 175, farfield mic and beamforming",
    "2026/02/18": "ESP32S3 Waveshare amoled 175, UI (fucked by bricked display)",
    "2026/02/19": "ESP32S3 POC code review",
    "2026/02/20": "Casual Leave",
    "2026/02/23": "ESP32S3 Waveshare power optimisation planning",
    "2026/02/24": "ESP32S3 Waveshare CI-CD",
    "2026/02/25": "ESP32S3 Waveshare OTA from CI-CD",
    "2026/02/26": "Exit from ZOMATO",
    "2026/02/27": "Entry to TEMPLE, Setup, Bone conduction IMU setup",
    "2026/02/28": "Bone conduction IMU demo to Deepi, Holi party",
    "2026/03/02": "BCM pipeline planning for testing, issue with noise",
    "2026/03/03": "BCM noise issue partial solve by different tape (single sided vs DST)",
    "2026/03/04": "BCM trying to solve noise and study papers",
    "2026/03/05": "Firmware dev env setup and reading",
    "2026/03/06": "BCM data collection application, and test pipeline",
    "2026/03/07": "Sensors datasheet go through",
    "2026/03/08": "Firmware reading",
    "2026/03/09": "BCM in-vehicle data, different ODR testing",
    "2026/03/10": "Piezo testing using BCM based heatmap",
    "2026/03/11": "LSM6DSV16BX IMU's I2C vs TDM noise analysis, piezo testing using BCM based heatmap",
    "2026/03/12": "LSM6DSV16BX IMU's I2C vs TDM noise analysis",
    "2026/03/13": "VAD (voice activity detection) research, Nucleo-G070RB board setup for TDM over SPI",
    "2026/03/14": "TDM over SPI research (Wont work due to freq mismatch)",
    "2026/03/16": "Reverse Engineering mems studio to STeval USB comms for creating custom audio recording pipeline app",
    "2026/03/17": "OpenEarable data from BMA580 mems accel (shitty)",
    "2026/03/18": "Compiling text samples for collecting STT dataset",
    "2026/03/19": "Power profiling BCM firmware, Studying Frequencies of sound",
    "2026/03/20": "Power profiling TDM vs I2C on LSM6DSV16BX",
    "2026/03/21": "Reverse engineering MemsStudio USB proto for task 20",
    "2026/03/23": "Studying MLC (Machine learning core) in LSM6DSV16BX",
    "2026/03/24": "Implement VAD on MLC (got it working)",
    # 2026/03/25 skipped intentionally
    "2026/03/26": "",
}

for key, task in TASKS.items():
    path = os.path.join(VAULT, key.replace("/", os.sep) + ".md")
    if not os.path.exists(path):
        print(f"MISSING: {path}")
        continue
    with open(path) as f:
        content = f.read()
    if task:
        new_content = re.sub(r'(# Tasks\n)-\s*\n', f'# Tasks\n- {task}\n', content, count=1)
    else:
        new_content = content  # leave blank (26.md)
    if new_content != content:
        with open(path, "w") as f:
            f.write(new_content)
        print(f"Updated: {key}")
    else:
        print(f"No change: {key}")
