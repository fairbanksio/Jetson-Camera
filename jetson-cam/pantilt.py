import time
from adafruit_servokit import ServoKit
from multiprocessing import Process

kit = ServoKit(channels=16)

pan = kit.servo[0]
pan_min = 2
pan_max = 154
pan_center = 93
pan_current = None

tilt = kit.servo[1]
tilt_min = 1
tilt_max = 130
tilt_center = 80
tilt_current = None

def center_camera():
    pan.angle = 93
    pan_current = 80
    tilt.angle = 80
    tilt_current = 80

def pan_sweep(min=pan_min, max=pan_max):
    while True:
        pan_minmax = max-(max%min)
        for i in range(pan_minmax,-1,-min):
            pan.angle = i
            pan_current = i
            time.sleep(0.05)
        for i in range(max+1):
            pan.angle = i
            pan_current = i
            time.sleep(0.05)

def tilt_sweep(min=tilt_min, max=tilt_max):
    while True:
        tilt_minmax = max-(max%min)
        for i in range(tilt_minmax,-1,-min):
            tilt.angle = i
            time.sleep(0.03)
        for i in range(max+1):
            tilt.angle = i
            tilt_current = i
            time.sleep(0.03)

def ptz_tracking():
    print("....")

if __name__=='__main__':
    try:
        panProc = Process(target=pan_sweep)
        panProc.start()

        tiltProc = Process(target=tilt_sweep)
        tiltProc.start()    

    except KeyboardInterrupt:
        center_camera()