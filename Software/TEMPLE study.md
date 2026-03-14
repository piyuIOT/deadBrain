# Project Overview: 
## Hardware Architecture
### 1. MCU: nRF52840
* **Memory:** 1MB Flash & 256 KB RAM
* **Storage:** QSPI Flash 64MB with Ring Buffer
* **Wireless:** BLE +8 dBM TX
* **Connectivity/Power:** 
	* USB DFU & charging (*Note: Remove USB part of firmware??*)
    * NFC touch to Pair support ?
    * Active RSSI base Tx power control ?
### 2. IMU: LSM6DSO
* **Interface:** SPI, I2C, I3C
* **Buffer:** 
	* 3KB FIFO buffer = 512 words / data points 
		* 1 Word  = 8 Bytes = 1byte Tag + 7byte Data
	* can go upto 9KB with onBoard compression (only if freq accel && freq gyro <= 1.66 kHz)
	* **INT FIFO:** INT1_CTRL
	* **Modes:**
		* **Continuous:** rolling buffer
		* **FIFO:** static oldest buffer (once filled, won't read new data)
	* **Compression `sec (9.10.3) in doc`:** change compression at runtime (compression for regular data > Normal for audio !!!)
	    * No compression for > 1.66 KHz freq (accel or gyro)
* **Features:**
	* Pedometer
	* step detector
	* step counter
    * Significant motion detection
    * relative tilt detection
    * **INT (Interrupts):** Free fall / wake up / tap / double tap / activity / inactivity / motion / stationary / 6D-4D orientation
    * 16 Programmable FSM (accel & gyro & ext sensor & temp sensor)
* **Power Modes:**
    * **ULP:** (Accel + ~~gyro~~) low speed
    * **LP:** (Accel + gyro) low speed
    * **High Perf:** (Accel + Gyro) high speed
    * *Note: Gyro is too much power (resonating mass!)*
* **Self Test:** accel self test !! & gyro self test !!
* **Digital & Analog Filtering:**
	* Analog Anti aliasing LPF In High Performance mode
	* Digital LPF1 in IMU (output data rate, ODR / 2) `(Pg 18 docs)`
		* 6660 Hz ≈ 3330 Hz audio LPF
	* Then put HPF
	    * ODR / 45 ≈ 74 HPF
### 3. PPG: MAX 86161
* **Buffer:** 128 word FIFO (3 Byte word)
* **Features:** 
	* Multi sample mode
	* on chip averaging
	* Proximity function
* **Power:**
    * **(ULP):** < 10 µA for 25 sps
    * **(Shut down cur):** ~ 1.6 µA (*LDO_EN=0 -> 0.05 µA*)
* **Optical Readout (Led Pulse):** 14.8 µs, 29.4 µs, 58.7 µs, 117.3 µs
* **Rates:** 
	* 8 sps to 4096 sps
    * (Low Power Mode) for < 256 sps
---
# Softwares