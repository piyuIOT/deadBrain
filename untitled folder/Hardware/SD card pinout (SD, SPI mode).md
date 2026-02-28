# SD card
![](assets/SD%20card%20pinout%20(SD,%20SPI%20mode)/sd_card_pinout.png)

| Pin | SD Mode   | SD Meaning                                                  | SPI Mode   | SPI Meaning                                             |
| --- | --------- | ----------------------------------------------------------- | ---------- | ------------------------------------------------------- |
| 1   | CD / DAT3 | Card Detect (when used) or Data Line 3 (bidirectional data) | CS         | Chip Select (active low, selects the card)              |
| 2   | CMD       | Command/response line (bidirectional)                       | DI / MOSI  | Data In (Master Out Slave In – data from host to card)  |
| 3   | VSS1      | Ground 1                                                    | GND        | Ground                                                  |
| 4   | VDD       | Power supply (usually 3.3 V)                                | VDD        | Power supply (usually 3.3 V)                            |
| 5   | CLK       | Clock (synchronizes data transfer)                          | SCLK / SCK | Serial Clock (provided by host)                         |
| 6   | VSS2      | Ground 2                                                    | GND        | Ground                                                  |
| 7   | DAT0      | Data Line 0 (primary bidirectional data line)               | DO / MISO  | Data Out (Master In Slave Out – data from card to host) |
| 8   | DAT1      | Data Line 1 (bidirectional, for 4-bit mode)                 | NC / IRQ   | Not Connected (or optional interrupt in some SDIO uses) |
| 9   | DAT2      | Data Line 2 (bidirectional, for 4-bit mode)                 | NC         | Not Connected                                           |
# MicroSD card
![](assets/SD%20card%20pinout%20(SD,%20SPI%20mode)/microSD_card_pinout.png)

| Pin | SD Mode   | SD Meaning                                                  | SPI Mode   | SPI Meaning                                             |
| --- | --------- | ----------------------------------------------------------- | ---------- | ------------------------------------------------------- |
| 1   | DAT2      | Data Line 2 (bidirectional, for 4-bit mode)                 | NC         | Not Connected                                           |
| 2   | CD / DAT3 | Card Detect (when used) or Data Line 3 (bidirectional data) | CS         | Chip Select (active low, selects the card)              |
| 3   | CMD       | Command/response line (bidirectional)                       | DI / MOSI  | Data In (Master Out Slave In – data from host to card)  |
| 4   | VDD       | Power supply (usually 3.3 V)                                | VDD        | Power supply (usually 3.3 V)                            |
| 5   | CLK       | Clock (synchronizes data transfer)                          | SCLK / SCK | Serial Clock (provided by host)                         |
| 6   | VSS       | Ground                                                      | GND        | Ground                                                  |
| 7   | DAT0      | Data Line 0 (primary bidirectional data line)               | DO / MISO  | Data Out (Master In Slave Out – data from card to host) |
| 8   | DAT1      | Data Line 1 (bidirectional, for 4-bit mode)                 | NC         | Not Connected                                           |
