### Initial Setup

`pip3 install opencv-python flask imutils adafruit_servokit`


### Launch & Usage

Basic start-up:

`python3 Jetson/jetson-cam/main.py`

Advanced start-up:

`python3 Jetson/jetson-cam/main.py --slack-token <MY SLACK TOKEN> --ptz-test --debug`

If you are testing and get a *Failed to start CaptureSession* error, restart the nvargus-daemon and retry:

`sudo systemctl restart nvargus-daemon`