# Jetson Camera

[![jetson-camera](https://assets.mofoprod.net/network/images/ring_banner.original.png)](https://www.eff.org/deeplinks/2020/02/what-know-you-buy-or-install-your-amazon-ring-camera)

### Ring cameras suck, so I'ma make my own

<hr>

### Wiring

**Jetson Pins**  ->  **Servo Driver Pins**
J41 Pin 3 (SDA)  ->  PCA9685 SDA
J41 Pin 5 (SCL)  ->  PCA9685 SCL
J41 Pin 1 (3.3V) ->  PCA9685 VCC
J41 Pin 6 (GND)  ->  PCA9685 GND

It is also recommended to use a separate [5v adapter](https://smile.amazon.com/BOLWEO-Universal-Connector-Household-Electronic/dp/B07QNTF9G8) to provide additional power for the servos. Pulling power from the Jetson itself can work for simple testing but heavier loads can damage the board. TLDR: Use a 5v adapter to power servos.


### Setup

`pip3 install opencv-python flask imutils adafruit_servokit`


### Usage

Basic start-up:

`python3 Jetson/jetson-cam/main.py`

Advanced start-up:

`python3 Jetson/jetson-cam/main.py --slack-token <MY SLACK TOKEN> --ptz-test --debug`

If you are testing and get a *Failed to start CaptureSession* error, restart the nvargus-daemon and retry:

`sudo systemctl restart nvargus-daemon`


### Hardware

- [Jetson Nano 2GB Developer Kit](https://smile.amazon.com/NVIDIA-Jetson-Nano-2GB-Developer/dp/B08J157LHH)
- Anker [USB C Power Adapter](https://smile.amazon.com/gp/product/B0828WB2VR) & [Power Cable](https://smile.amazon.com/gp/product/B0832M47KX)
- [Raspberry Pi v2 Camera](https://smile.amazon.com/Raspberry-Pi-Camera-Module-Megapixel/dp/B01ER2SKFS) - v1 cameras will **not** work; v2 is required
- [16-Channel I2C Servo Driver](https://smile.amazon.com/gp/product/B014KTSMLA) - boards with fewer channels will work as well
- [2 x Tower Pro SG92R Servos](https://smile.amazon.com/TowerPro-SG92R-Micro-Servo-pack/dp/B01CX63AOQ/)
- [Female-to-Female Jumper Wires](https://smile.amazon.com/gp/product/B01L5ULRUA)
- [5v Power Adapter](https://smile.amazon.com/BOLWEO-Universal-Connector-Household-Electronic/dp/B07QNTF9G8) - used to power servos; powering them via GPIO is not recommended
- Optional: [40mm PWM Fan](https://smile.amazon.com/dp/B07DXS86G7) - although a fan is not required, Nvidia does recommend this Noctua for the Nano


### Resources
- Jetson Nano
    - Getting Started: https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit
    - Header Pinout: https://www.jetsonhacks.com/nvidia-jetson-nano-j41-header-pinout
- Video Capture
    - OpenCV Video: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
- PTZ
    - I2C Servos: https://www.jetsonhacks.com/2019/07/22/jetson-nano-using-i2c
    - ServoKit docs: https://circuitpython.readthedocs.io/projects/servokit/en/latest/api.html
- Notifications
    - Slack Block Kit Builder: https://app.slack.com/block-kit-builder
- What's wrong with Ring?
    - EFF What to Know: https://www.eff.org/deeplinks/2020/02/what-know-you-buy-or-install-your-amazon-ring-camera
    - Backdoor Access: https://www.eff.org/deeplinks/2020/11/police-will-pilot-program-live-stream-amazon-ring-cameras
    - 3rd Party Data Sharing: https://www.latimes.com/business/technology/story/2020-01-29/ring-app-shares-personal-data-eff-finds
    

### To Do

- [ ] Properly close the stream
- [x] Face/Person Detection
- [x] Improve Detection FPS
- [ ] PTZ Support
- [x] Notifications
- [ ] Refactor