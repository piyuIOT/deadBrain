# Pipeline:
```mermaid
flowchart TD
  
A[Input<br/>IMU Bone Conduction Mic<br/>Air Conduction Mic<br/>Piezo Bone Conduction Mic]  
  
B[VAD Detection<br/>Low Power: Hardware VAD<br/>Medium Power: VAD Silicon<br/>High Power: MCU Software]  
  
C[Start Wakeword Engine<br/>Detect Speech Start]  
  
D[Start Audio Streaming<br/>Recording / STT Pipeline]  
  
E[VAD Detects Silence]  
  
F[Power Down<br/>Wakeword Engine + Speech Pipeline]  
  
A --> B  
B --> C  
C --> D  
D --> E  
E --> F
```
# Options:
- **MEMS Accelerometer-Only Solution** ODR up to 6.8kHz with hardware VAD support (same IMU used for bone conduction by openEarable) Package size: 1.2 × 0.8 × 0.55 mm → [BMA580 Datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bma580-ds000.pdf)
- **VAD Chip** _(requires mic input via I2S or PDM, not TDM — doubles power draw: mic + VAD chip)_ → [NeuroVoice VAD Product Brief](https://polyn.ai/wp-content/uploads/2024/03/NeuroVoice-VAD-Product-Brief-v08-5.pdf)
- **Onboard VAD & `Wake Word` Microphones**
	1. [SISTC Smart MEMS Microphone](https://sistc.com/product/smart-mems-microphone/)
	2. [Knowles SmartMic — used in vivo NEX AI Smartphone](https://investor.knowles.com/news/news-details/2018/Vivo-Selects-Knowles-SmartMic-in-New-Flagship-vivo-NEX-AI-Smartphone-06-12-2018/default.aspx)
	3. [Knowles IA611 Datasheet](https://www.knowles.com/docs/default-source/default-document-library/zz_ia611-datasheet-2019-brochure.pdf?sfvrsn=fd4871b1_2)
### LSM6DSV16BX based solution
```mermaid
flowchart TD
    subgraph Z1["Always-on sensing + VAD · 190 µA · high-performance mode"]
        IMU["LSM6DSV16BX I2C / TDM · 960 Hz · 190 µA · high-performance mode"]
        VAD["MLC-based VAD decision tree · UI / I2C path — not TDM"]

        subgraph MLC["MLC internal flow"]
            TDSA["① TDSA blocks — Time Domain Statistical Analysis mean · variance · energy · zero-crossing rate ST-provided fixed block set"]
            DT["② Decision tree evaluates feature vectors result written to MLC output register"]
            GINT["③ MLC INT pin asserts GPIO interrupt sent to MCU"]
            TDSA -- feature vectors --> DT
            DT -- output register set --> GINT
        end

        MCU["MCU starts TDM interface on IMU MCU already active · GPIO INT triggers TDM enable only"]

        IMU --> VAD
        VAD --> TDSA
        GINT --> MCU
    end

    MCU -- VAD trigger detected --> WW

    subgraph Z2["Conditional — active only on VAD trigger"]
        WW["Wake word engine CNN / keyword spotting powered on by VAD trigger only"]
        SB["sleep / standby TDM off · VAD re-arms"]
        WW -- if no wake word detected --> SB
    end

    WW -- keyword match --> AUD

    subgraph Z3["Active pipeline — speech recording + STT"]
        AUD["Begin audio capture TDM stream from IMU · ring buffer"]
        STT["Speech-to-text pipeline streaming or batch · on-device or cloud ASR"]
        SIL["Silence / end-of-speech detection VAD detects sustained silence · speech segment ends"]
        AUD --> STT
        STT --> SIL
    end

    SIL -- back to sleep/standby · TDM off · VAD re-arms --> SB
```

OR more visually appealing:

![](assets/VAD%20(voice%20activity%20detection)/IMU%20MLC%20VAD.png)