import cv2
from datetime import datetime
import time
import threading
from flask import Response, Flask

global video_frame
video_frame = None

global thread_lock 
thread_lock = threading.Lock()

HAAR_CASCADE_XML_FILE = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
#HAAR_CASCADE_XML_FILE = "/usr/share/opencv4/haarcascades/haarcascade_upperbody.xml"
#HAAR_CASCADE_XML_FILE = "/usr/share/opencv4/haarcascades/haarcascade_fullbody.xml"

#GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1920, height=1080, format=(string)NV12, framerate=30/1 ! nvvidconv flip-method=2 ! video/x-raw, format=(string)BGRx ! videoconvert ! appsink'
GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=1848, format=(string)NV12, framerate=28/1 ! nvvidconv flip-method=2 ! video/x-raw, width=1680, height=1050, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'

app = Flask(__name__)

def captureFrames():
    global video_frame, thread_lock
    video_capture = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)
    while True and video_capture.isOpened():
        return_key, frame = video_capture.read()
        if not return_key:
            break

        with thread_lock:
            video_frame = frame.copy()

        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break

    video_capture.release()

def detectMotion():
    global video_frame
    cascade = cv2.CascadeClassifier(HAAR_CASCADE_XML_FILE)
    while True:
        global video_frame

        if video_frame is None:
            continue

        grayscale_image = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
        detected = cascade.detectMultiScale(grayscale_image, 1.3, 5)

        if any(map(len, detected)):
            now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            print(f"[{now}] Motion Detected")
        for (x_pos, y_pos, width, height) in detected:
            cv2.rectangle(video_frame, (x_pos, y_pos), (x_pos + width, y_pos + height), (0, 0, 255), 2)
        
def encodeFrame():
    global thread_lock
    while True:
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            return_key, encoded_image = cv2.imencode(".jpg", video_frame)
            if not return_key:
                continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n') # Output image as a byte array

@app.route("/")
def streamFrames():
    return Response(encodeFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    process_thread = threading.Thread(target=captureFrames)
    process_thread.daemon = True

    detect_thread = threading.Thread(target=detectMotion)
    detect_thread.daemon = True

    process_thread.start()
    detect_thread.start()

    app.run("0.0.0.0", port="8000")