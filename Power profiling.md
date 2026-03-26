IMU only, no gyro:
- HP (2-16 g & 7.5-7.6 kHz) --> 960 uA - 1040 uA
- LP1 (2-16 g & 1.875-240 Hz) -->  --> 770 uA - 820 uA
- LP2 (2-16 g & 1.875-240 Hz) -->  1.875 Hz - 240 Hz --> 770 uA - 830 uA
- LP3 (2-16 g & 1.875-240 Hz) --> 1.875 Hz - 240 Hz --> 770 uA - 850 uA
- TDM --> 8 kHz --> 1250 uA (upto 30 uA less for 8g scale then in 2g scale)
- TDM --> 16 kHz --> 1400 uA (upto 60 uA less for 8g scale then in 2g scale)
- HP + TDM (8 kHz) --> 1450 uA - 1600 uA
- HP + TDM (16 kHz) --> 1600 uA - 1750 uA

Complete module:


---

accel z axis only
480hz
960hz
band pass from 80-300


OYY TEMPLE	
OY IY T EH M P AH L


---

issue with piezo BCM accel setup
accel shows lower g reading on lower frequencies (vibration in bcm gives same output in piezo though, which is directly proportional to dispacement)
displacement is a function of frequency 
$$  
Displacementx(t) = A sin(ωt + φ)
$$$$
Velocityv(t) = Aω cos(ωt + φ)
$$$$
Accelerationa(t) = −Aω² sin(ωt + φ)
$$

That omega squared term gives us change in g readings in various frequency ranges