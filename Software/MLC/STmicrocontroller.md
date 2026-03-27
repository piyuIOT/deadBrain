- ST programming toolchain:
	1. CubeMX (MCU config tool)
	2. CubeIDE or VScode extension (for development)
	3. CubeProgrammer (Flashing tool)
	4. CubeMonitor (Monitoring)
- ST tool chain for AI:
	![](assets/STmicrocontroller/image_0kVUelgxRn.avif)
- Using ST MEMS Studio:
	1. [Playlist](https://www.youtube.com/playlist?list=PLnMKNibPkDnGdZACZFVUZGCe0Eq2y3wki)
- Using MLC: 
	1. [Video (short)](https://www.st.com/content/dam/videos-cf/pub/2025/q1/automatic-filter-selection-for-machine-learning-core-config-in-mems-studio.mp4)
	2. [Video](https://www.youtube.com/watch?v=v28k4Fy4tXc&list=PLnMKNibPkDnGdZACZFVUZGCe0Eq2y3wki&index=6)
	3. [Github](https://github.com/STMicroelectronics/st-mems-machine-learning-core)

LSM6DSV16BX MLC features:
- MLC ODR (MLC input data rate, if sensor ODR is higher than MLC will decimate data without filtering): 30, 60, 120, 240, 480, 960 Hz
- window length (number of samples to take for a computation): 1-255
- Accel FS support: +- 2, 4, 8, 16g
- Accel ODR: 15, 30, 60, 120, 240, 480, 960, 1920, 3840, 7680 Hz
- Filters (apply any 1): HP, BP, 1st order IIR, 2nd order IIR ON (xyz, rootSquaredSum, squaredSum)
- Features (any feature can be taken on the unfiltered data + rootSquaredSum of data + squaredSum of data + filtered data line `which can be filtered axis, or filtered rootSquaredSum or filtered squaredSum of axises`) in absolute or direct format:
	- Mean
	- Variance
	- Energy
	- Peak-to-peak
	- zero-crossing
	- positive zero-crossing
	- negative zero-crossing
	- peak detector
	- positive peak detector
	- negative peak detector
	- minimum
	- maximum
	- recursive mean and variance and rms
	- recursive min and max and peak to peak
- Binary decision tree: $feature\ coputed\ over\ win\ length > < = fixed\ value$ 
- Meta classifier: 0 - 14