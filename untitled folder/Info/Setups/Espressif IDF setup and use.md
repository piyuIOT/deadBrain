# Setup
ESP_IDF (Espressif Integrated development framework) + VSCode (no extensions, no ESP-IDE, no platformIO, no arduino nothing!)
1. [Install preReqs](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/macos-setup.html)
2. Then Install [EIM cli](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/macos-setup.html#step-2-install-the-eim)
3. Then [Install IDF from EIM cli](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/macos-setup.html#online-installation-using-eim-cli)

> [!info]
> If you face issue with EIM unable to detect python, create the following symlinks maybe
> ```zsh
>	sudo ln -sf /opt/homebrew/bin/python3.12 /usr/local/bin/python
>	sudo ln -sf /opt/homebrew/bin/python3.12 /usr/local/bin/python3
>	sudo ln -sf /opt/homebrew/bin/python3.12 /usr/local/bin/python312
> ```
> and then export path and create alias in .zshrc by adding this
> ```zsh
>	export PATH="$HOME/.local/bin:$PATH"
>	export PATH="/opt/homebrew/bin:$PATH"
>	alias python3='/opt/homebrew/bin/python3.12'
>	alias pip3='/opt/homebrew/bin/pip3.12'
> ```
# Usage
1. Every time to start working in IDF you need to source it, so creating a alias is a good idea by adding this to you ~/.zshrc
```zsh
alias sourceEspIdf='source "/Users/<username>/.espressif/tools/activate_idf_v<yourVersion>.sh"'
```

---
- [Official espressif guide for installations](https://docs.espressif.com/projects/espressif-ide/en/latest/installation.html)
- [Tutorial for running hello world in ESP32](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/linux-macos-setup.html)

Write about:
- idf (from cli)
- options for devlopment: ide, vscode extension, vscode platformio extension, etc

document the procedure for building in cli
https://docs.espressif.com/projects/esp-idf/en/latest/esp32p4/get-started/linux-macos-start-project.html

this has 
source env, 
set target, 
all about menu config,
build firmware, 
flash firmware, 
clear flash 
etc

