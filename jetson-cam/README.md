# Jetson Camera

Ring cameras suck, so I'ma make my own

## Usage 
`sudo systemctl restart nvargus-daemon && clear && python3 Jetson/jetson-cam/main.py`

Why restart the daemon every time? [More Background](https://forums.developer.nvidia.com/t/nvarguscamerasrc-plugin-error/75814/14)

## To Do

- [ ] Properly close the stream
- [x] Face/Person Detection
- [x] Improve Detection FPS
- [ ] PTZ Support
- [x] Notifications

## Resources
- Video Capture
    - OpenCV Video: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
- PTZ
    - I2C Servos: https://www.jetsonhacks.com/2019/07/22/jetson-nano-using-i2c/
    - ServoKit docs: https://circuitpython.readthedocs.io/projects/servokit/en/latest/api.html 