# Jetson Camera

Ring cameras suck, so I'ma make my own

## Usage
`python3 Jetson/jetson-cam/main.py`

If you are testing and get a *Failed to start CaptureSession* error, restart the nvargus-daemon and retry:
`sudo systemctl restart nvargus-daemon`

## To Do

- [ ] Properly close the stream
- [x] Face/Person Detection
- [x] Improve Detection FPS
- [ ] PTZ Support
- [x] Notifications
- [ ] Refactor

## Resources
- Video Capture
    - OpenCV Video: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
- PTZ
    - I2C Servos: https://www.jetsonhacks.com/2019/07/22/jetson-nano-using-i2c/
    - ServoKit docs: https://circuitpython.readthedocs.io/projects/servokit/en/latest/api.html
- Notifications
    - Slack Block Kit Builder: https://app.slack.com/block-kit-builder