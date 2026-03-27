# Current hardware setup
- [STEVAL-MKI237KAB](https://www.st.com/en/evaluation-tools/steval-mki237ka.html) board (contains [LSM6DSV16BX](https://www.st.com/en/mems-and-sensors/lsm6dsv16bx.html) IMU)
- STEVAL-MKIGI06AB is just a connector board (no processing/ no actives/ no passives)
- [STEVAL-MKI109D](https://www.st.com/en/evaluation-tools/steval-mki109d.html) plug and play evaluation board

> Software used is ST MEMS Studio, connect via usb, select serial com, select board and IMU, configure to one of the following mode (UI for regular IMU, TDM for BCM) and then either record or check FFT and graphs 
# Bone Conduction Data set: 
1. https://vibravox.cnam.fr/index.html
2. https://github.com/wangmou21/abcs
# Software resources:
[IMU driver](https://github.com/STMicroelectronics/lsm6dsv16bx-pid/tree/main)
[ST Mems github](https://github.com/STMicroelectronics/STMems_Standard_C_drivers/tree/master/lsm6dsv16bx_STdC)
[IMU arduino driver](https://github.com/stm32duino/LSM6DSV16BX-TDM)

