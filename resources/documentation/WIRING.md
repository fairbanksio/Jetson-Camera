### Servo Wiring

<img src="https://raw.githubusercontent.com/Fairbanks-io/Jetson/main/resources/images/pinout.png" width="40%" height="40%" />

| Jetson Pins (J41) | Servo Driver Pins (PCA9685) |
|-------------------|-----------------------------|
| Pin 3 (SDA)       | SDA (Data)                  |
| Pin 5 (SCL)       | SCL (Clock)                 |
| Pin 1 (3.3v)      | VCC (Power)                 |
| Pin 6 (GND)       | GND (Ground)                |

It is also recommended to use a separate [5v adapter](https://smile.amazon.com/BOLWEO-Universal-Connector-Household-Electronic/dp/B07QNTF9G8) to provide additional power for the servos. Pulling power from the Jetson itself can work for simple testing but heavier loads can damage the board. 

TLDR: Use a 5v adapter to power servos.