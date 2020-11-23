# Jetson Camera

#### Ring cameras suck, so I'ma make my own

## Usage

`python3 Jetson/jetson-cam/main.py`

If you are testing and get a *Failed to start CaptureSession* error, restart the nvargus-daemon and retry:
`sudo systemctl restart nvargus-daemon`


## Hardware

- [Jetson Nano 2GB Developer Kit](https://smile.amazon.com/NVIDIA-Jetson-Nano-2GB-Developer/dp/B08J157LHH)
- Anker [USB C Power Adapter](https://smile.amazon.com/gp/product/B0828WB2VR) & [Power Cable](https://smile.amazon.com/gp/product/B0832M47KX)
- [Raspberry Pi v2 Camera](https://smile.amazon.com/Raspberry-Pi-Camera-Module-Megapixel/dp/B01ER2SKFS)
- [16-Channel I2C Servo Driver](https://smile.amazon.com/gp/product/B014KTSMLA)
- [2 x Tower Pro SG92R Servos](https://smile.amazon.com/TowerPro-SG92R-Micro-Servo-pack/dp/B01CX63AOQ/)
- [Female-to-Female Jumper Wires](https://smile.amazon.com/gp/product/B01L5ULRUA)


## Resources

- Video Capture
    - OpenCV Video: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
- PTZ
    - I2C Servos: https://www.jetsonhacks.com/2019/07/22/jetson-nano-using-i2c/
    - ServoKit docs: https://circuitpython.readthedocs.io/projects/servokit/en/latest/api.html
- Notifications
    - Slack Block Kit Builder: https://app.slack.com/block-kit-builder


## To Do

- [ ] Properly close the stream
- [x] Face/Person Detection
- [x] Improve Detection FPS
- [ ] PTZ Support
- [x] Notifications
- [ ] Refactor