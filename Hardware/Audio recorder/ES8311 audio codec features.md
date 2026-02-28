# 10.3 HIGH PASS FILTER, VOLUME CONTROLS, ALC AND EQUALIZER
The digital output of mono ADC is fed into a DSP block which has features including high pass filter, volume control, ALC and equalizer.
## 10.3.1 HIGH PASS FILTER
ADC_HPF controlled by Reg0x1C.Bit[5] is used to freeze or active internal high pass filter. This high pass filter can cancel the DC offset in digital domain. ADC_HPFS1 and ADC_HPFS2 is the coefficient of high pass filter. The frequency response of this filter will be updated if the coefficient has been changed. This high pass filter can be used to attenuate low-frequency noise if the suitable coefficient is used for it.

ADC_HPF = '1' actives this high pass filter and set it into dynamic mode. In this mode, the DC offset will be canceled dynamically, and it will slightly decrease SNR of ADC.

ADC_HPF = '0' freezes this high pass filter. In this mode, the DC offset is frozen and a constant DC offset exists in digital domain. If there is a constant DC offset in application, ADC_HPF can be cleared to freeze DC offset.

Also, this high pass filter can be disabled with two methods as following.

1. Clear ADC_HPF to '0' before the state machine startup. It will freeze DC offset to zero.
2. Set ADC_RAMCLR to '1' when ADC_HPF has been cleared to '0'. It will clear all data in RAM, including DC offset.
### Register 0X16 – ADC, DEFAULT 0000 0100

| Bit        | Name | Bit Description                         |
| ---------- | ---- | --------------------------------------- |
| ADC_RAMCLR | 3    | adc ram clear when lrck/adc_mclk active |
### Register 0X1B – ADC, DEFAULT 0000 1100

| Bit       | Name | Bit Description     |
| --------- | ---- | ------------------- |
| ADC_HPFS1 | 4:0  | ADCHPF stage1 coeff |
### Register 0X1C – ADC, DEFAULT 0100 1100

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADC_HPF | 5 | ADC offset freeze<br>0 – freeze offset<br>1 – dynamic HPF |
| ADC_HPFS2 | 4:0 | ADCHPF stage2 coeff |
## 10.3.2 VOLUME CONTROL AND ALC
ES8311 ADC has a digital volume register and ALC (automatic level control) registers. ADC_VOLUME controlled by register 0x17 is used for digital volume.

If ALC is enabled, the ADC_VOLUME register is the max gain of ALC, and the recording volume depends on ALC.

If ALC is disabled, the recording volume is controlled by ADC_VOLUME register. The digital volume has a range from -95.5dB to +32dB with a resolution in 0.5dB/step.
### Register 0X17 – ADC, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADC_VOLUME | 7:0 | ADC volume<br>0x00 – -95.5dB (default)<br>0x01 – -90.5dB<br>… 0.5dB/step<br>0xBE – -0.5dB<br>0xBF – 0dB<br>0xC0 – +0.5dB<br>…0xFF – +32dB |
### Register 0X18 – ADC, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ALC_EN | 7 | ADC auto level control enable<br>0 – ALC disable(default)<br>1 – ALC enable |
| ADC_AUTOMUTE_EN | 6 | ADC automute enable<br>0 – automute disable(default)<br>1 – automute enable |
| ALC_WINSIZE | 3:0 | winsize for alc<br>cnt_timer[ALC_WINSIZE]<br>0 – 0.25dB/2LRCK<br>1 – 0.25dB/4LRCK<br>... 15 – 0.25dB/65536LRCK |
### Register 0X19 – ADC, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ALC_MAXLEVEL | 7:4 | ALC target max level<br>0 – -30.1dB<br>1 – -24.1dB<br>2 – -20.6dB<br>3 – -18.1dB<br>4 – -16.1dB<br>5 – -14.5dB<br>6 – -13.2dB<br>7 – -12.0dB<br>8 – -11.0dB<br>9 – -10.1dB<br>10 – -9.3 dB<br>11 – -8.5 dB<br>12 – -7.8 dB<br>13 – -7.2 dB<br>14 – -6.6 dB<br>15 – -6.0 dB |
| ALC_MINLEVEL | 3:0 | ALC target min level<br>0 – -30.1dB<br>1 – -24.1dB<br>2 – -20.6dB<br>3 – -18.1dB<br>4 – -16.1dB<br>5 – -14.5dB<br>6 – -13.2dB<br>7 – -12.0dB<br>8 – -11.0dB<br>9 – -10.1dB<br>10 – -9.3 dB<br>11 – -8.5 dB<br>12 – -7.8 dB<br>13 – -7.2 dB<br>14 – -6.6 dB<br>15 – -6.0 dB |
### Register 0X1A – ADC, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADC_AUTOMUTE_WS | 7:4 | ADC automute winsize<br>Detect samples= (2^11)*(winsize+1)<br>0 – 2048 samples - 42ms<br>1 – 4096 samples - 84ms<br>... 15 – 32768 samples - 688ms |
| ADC_AUTOMUTE_NG | 3:0 | ADC automute noise gate<br>0 – -96dB<br>1 – -90dB<br>2 – -84dB<br>3 – -78dB<br>4 – -72dB<br>5 – -66dB<br>6 – -60dB<br>7 – -54dB<br>8 – -51dB<br>9 – -48dB<br>10 – -45dB<br>11 – -42dB<br>12 – -39dB<br>13 – -36dB<br>14 – -33dB<br>15 – -30dB |
## 10.3.3 EQUALIZER
ES8311 ADC has an equalizer which is a 2nd filter. This equalizer can be programmed as low pass filter or high pass filter. A band-pass filter can be realized if this equalizer has been combined with the high pass filter descripted in section 10.3.1.

If this equalizer is used for ADC recording, the clock ratio between internal ADC MCLK and LRCK must be equal or greater than 256.

This equalizer can be bypassed if ADC_EQBYPASS is set to '1'. In this mode, the clock ratio between internal ADC MCLK and LRCK must be equal or greater than 240.

Register 0x1E to Register 0x30 are all the coefficient of equalizer. Everest can provide a tool to calculate the coefficient of equalizer. You can get this tool from Everest Semiconductor co., Ltd.
### Register 0X1C – ADC, DEFAULT 0100 1100

| Bit          | Name | Bit Description                                    |
| ------------ | ---- | -------------------------------------------------- |
| ADC_EQBYPASS | 6    | ADCEQ bypass<br>0 – normal<br>1 – bypass (default) |
### Register 0X1D – ADC, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_B0[29:24] | 5:0 | 30-bit B0 coefficient for ADCEQ |
### Register 0X1E – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_B0[23:16] | 7:0 | 30-bit B0 coefficient for ADCEQ |
### Register 0X1F – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_B0[15:8] | 7:0 | 30-bit B0 coefficient for ADCEQ |
### Register 0X20 – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_B0[7:0] | 7:0 | 30-bit B0 coefficient for ADCEQ |
### Register 0X21 – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_A1[29:24] | 7:0 | 30-bit A1 coefficient for ADCEQ |
### Register 0X22 – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_A1[23:16] | 7:0 | 30-bit A1 coefficient for ADCEQ |
### Register 0X23 – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_A1[15:8] | 7:0 | 30-bit A1 coefficient for ADCEQ |
### Register 0X24 – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_A1[7:0] | 7:0 | 30-bit A1 coefficient for ADCEQ |
### Register 0X25 – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_A2[29:24] | 7:0 | 30-bit A2 coefficient for ADCEQ |
### Register 0X26 – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_A2[23:16] | 7:0 | 30-bit A2 coefficient for ADCEQ |
### Register 0X27 – ADCEQ, DEFAULT 0000 0000

| Bit            | Name | Bit Description                 |
| -------------- | ---- | ------------------------------- |
| ADCEQ_A2[15:8] | 7:0  | 30-bit A2 coefficient for ADCEQ |
### Register 0X28 – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_A2[7:0] | 7:0 | 30-bit A2 coefficient for ADCEQ |
### Register 0X29 – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_B1[29:24] | 7:0 | 30-bit B1 coefficient for ADCEQ |
### Register 0X2A – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_B1[23:16] | 7:0 | 30-bit B1 coefficient for ADCEQ |
### Register 0X2B – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_B1[15:8] | 7:0 | 30-bit B1 coefficient for ADCEQ |
### Register 0X2C – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_B1[7:0] | 7:0 | 30-bit B1 coefficient for ADCEQ |
### Register 0X2D – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_B2[29:24] | 7:0 | 30-bit B2 coefficient for ADCEQ |
### Register 0X2E – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_B2[23:16] | 7:0 | 30-bit B2 coefficient for ADCEQ |
### Register 0X2F – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_B2[15:8] | 7:0 | 30-bit B2 coefficient for ADCEQ |
### Register 0X30 – ADCEQ, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADCEQ_B2[7:0] | 7:0 | 30-bit B2 coefficient for ADCEQ |

---
# 10.6 ADC SPEED MODE, ADC OVER SAMPLE RATE AND ADC SCALE
The ADC in ES8311 can work in single speed or double speed mode. ADC_FSMODE = '0' selects single speed mode and ADC_FSMODE = '1' selects double speed mode.

ADC_OSR is the definition of ADC over sample rate. OSR must be equal or greater than 15 in single speed mode, and must be equal or greater than 16 in double speed mode. So please don't set ADC_OSR to the value equal or lower than 14. Below is the equation of ADC_OSR. The default of ADC OSR is 32.

1. Single speed, OSR = (internal adc mclk) ÷ LRCK ÷ 8
2. Double speed, OSR = (internal adc mclk) ÷ LRCK ÷ 4
### Register 0x03 – CLOCK MANAGER, DEFAULT 0001 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADC_FSMODE | 6 | adc fs mode<br>0 – single speed(default)<br>1 – double speed |
| ADC_OSR | 5:0 | ADC delta sigma over sample rate<br>0~14 – not use<br>15 – 60*fs(ss) / (ds not support)<br>16 – 64*fs(ss) / 32*fs(ds) (default)<br>... 31 – 124*fs(ss) / 62*fs(ds)<br>32 – 128*fs(ss) / 64*fs(ds)<br>... 63 – 252*fs(ss) / 126*fs(ds) |
ADC OSR will affect amplitude of the digital signal out from ADC. The smaller ADC OSR, the lower signal amplitude.

ADC_SCALE can compensate the amplitude for the ADC digital signal if the ADC OSR is lower than default. If ADC_SCALE isn't used for compensation while small number for OSR, the SNR of ADC will be lower than default because of the small amplitude.
### Register 0X16 – ADC, DEFAULT 0000 0100

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADC_SCALE | 2:0 | ADC gain scale up<br>0 - 0dB<br>1 - 6dB<br>2 - 12dB<br>3 - 18dB<br>4 - 24dB (default)<br>5 - 30dB<br>6 - 36dB<br>7 - 42dB |

---
# 10.7 FADE IN AND FADE OUT
ES8311 ADC has a fade in and fade out feature. ADC_RAMPRATE can enable or disable fade in and fade out feature, and select the ramp rate.
### Register 0X15 – ADC, DEFAULT 0000 0000

| Bit | Name | Bit Description |
|-----|------|-----------------|
| ADC_RAMPRATE | 7:4 | ADC VC ramp rate<br>0 - disable softramp<br>1 - 0.25dB/4LRCK<br>2 - 0.25dB/8LRCK<br>3 - 0.25dB/16LRCK<br>4 - 0.25dB/32LRCK<br>5 - 0.25dB/64LRCK<br>6 - 0.25dB/128LRCK<br>7 - 0.25dB/256LRCK<br>8 - 0.25dB/512LRCK<br>9 - 0.25dB/1024LRCK<br>10 - 0.25dB/2048LRCK<br>11 - 0.25dB/4096LRCK<br>12 - 0.25dB/8192LRCK<br>13 - 0.25dB/16384LRCK<br>14 - 0.25dB/32768LRCK<br>15 - 0.25dB/65536LRCK |
