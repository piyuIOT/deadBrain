# Hardware
## The dev kit in itself contains various sensors :
- 2 digital mic
- 2 analog mic
- baro and temp
- humidity and temp
- 6 axis imu
- 3 axis magnetometer
- 60ghz radar
- camera
## And connectors:
- mipi display connector
- speaker connection pad
- capacitive touch panel connector pad
## Default code:
2 default example codes on board:
- gesture detection using radar
- simple voice assistant
	- This voice assistant contains wakeword detection and command matching in it:
		- [Deepcraft voice assistant](https://deepcraft-voice-assistant.infineon.com/dashboard), its info [page](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions/deepcraft-audio-enhancement) and [doc](https://deepcraft-voice-assistant.infineon.com/DVA_User_Guide_new_branding.pdf) (this has no relation to Deepcraft AI studio, it a different web based tool):
			- [Voice assistant demo video](https://www.youtube.com/watch?v=hAXSKi1HxYU)
			- [Audio Enhancement demo video](https://www.youtube.com/watch?v=kS_WzyXqUTI)
# Toolchain


- [modusToolbox](https://www.infineon.com/design-resources/development-tools/sdk/modustoolbox-software) for programming, debugging, flashing etc (available as vscode extension as well, toolbox contains a lot more application for various individual tasks)
- [Deepcraft AI studio](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions/deepcraft-studio) (windows only) which is for machine learning model creation, conversion, optimisation. (Youtube playlist)
# Programming
- [Primary library](https://github.com/Infineon/TARGET_KIT_PSE84_AI)
- Learning resources basic programming:
	- [Overview](https://github.com/Infineon/mtb-training-psoc-edge-e84-introduction)
	- [Basic blink code](https://github.com/Infineon/mtb-training-psoc-edge-e84-intro-ecosystem)
	- [Deep dive into features](https://github.com/Infineon/mtb-training-psoc-edge-e84-features)
	- 
# MISC
- [Github infineon wakeword word and command detection model](https://github.com/Infineon/mtb-example-psoc6-dual-cpu-cyberon-freertos?tab=readme-ov-file)
- [Live remote hardware testing lab](https://infineon-live-lab.tenxerlabs.com/app/psoc-edge-e84)
- [Deepcraft AI hub](https://deepcraft.infineon.com/)
	- [Baby cry detection](https://deepcraft.infineon.com/models/DEEPCRAFTReadyModelforBabyCryDetection)
	- [Human activity detection](https://deepcraft.infineon.com/models/DEEPCRAFTStudioAcceleratorforHumanActivityDetection)
	- [Snoring detection](https://deepcraft.infineon.com/models/DEEPCRAFTReadyModelforSnoreDetection)
	- [Voice assistant](https://deepcraft.infineon.com/models/DEEPCRAFTVoiceAssistant)
	- [Cough detection](https://deepcraft.infineon.com/models/DEEPCRAFTReadyModelforCoughDetection)
	- [Audio enhancement](https://deepcraft.infineon.com/models/DEEPCRAFTAudioEnhancement)