import argparse
import cv2
from datetime import datetime
from notifications import post_message_to_slack
from notifications import post_file_to_slack
import os
import time
import threading
from flask import Response, Flask

__version__ = "1.0.5"

parser = argparse.ArgumentParser(description="Ring cameras suck, so I'ma make my own")
parser.add_argument("--debug", help="Increase output verbosity", action="store_true")
parser.add_argument("-v", "--version", help="Current Jetson Camera version.", action="store_true")
parser.add_argument("--slack-token", help="Slack bot token to be used for notifications")
parser.add_argument("--notification-delay", help="Interval in seconds between notifications", default=60)
parser.add_argument("--disable-motion", help="Disable motion detection", action="store_true")
parser.add_argument("--ptz-test", help="Verify PTZ functionality and range", action="store_true")
parser.add_argument("--port", help="Web Port", default=8000)
parser.add_argument("--save", help="Archive detected motion", action="store_true")
args = parser.parse_args() 

global video_frame
video_frame = None

global thread_lock 
thread_lock = threading.Lock()

global last_notify_time
last_notify_time = datetime.now()

global last_detected_location 

HAAR_CASCADE_XML_FILE = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
#HAAR_CASCADE_XML_FILE = "/usr/share/opencv4/haarcascades/haarcascade_upperbody.xml"
#HAAR_CASCADE_XML_FILE = "/usr/share/opencv4/haarcascades/haarcascade_fullbody.xml"

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
            if args.debug:
                # Draw a dot center screen
                center_coordinates = (840, 525)
                radius = 5
                center_color = (0, 255, 0)
                detected_color = (255, 0, 0)
                thickness = -1
                cv2.circle(video_frame, center_coordinates, radius, center_color, thickness)

        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break

    video_capture.release()

def detectMotion():
    global video_frame, last_notify_time, last_detected_location
    cascade = cv2.CascadeClassifier(HAAR_CASCADE_XML_FILE)
    while True:
        global video_frame

        if video_frame is None:
            continue

        grayscale_image = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
        detected = cascade.detectMultiScale(grayscale_image, 1.3, 5)

        # Figure out the timestamp
        date = datetime.now().strftime("%m/%d/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        
        # There's a person in the image
        for (x_pos, y_pos, width, height) in detected:
            someone_here = True
            if args.debug:
                detection_center = (int(x_pos + width / 2), int(y_pos + height / 2))
                print(f"[{time}] Motion Detected @ {detection_center}")
                last_detected_location = detection_center
                radius = 10
                color = (0, 0, 255)
                thickness = 2
                with thread_lock:
                    cv2.circle(video_frame, detection_center, radius, color, thickness)

            # Move to the detection
            center_coordinates = (840, 525)
            move_x = int(center_coordinates[0] - last_detected_location[0])
            move_y = int(center_coordinates[1] - last_detected_location[1])
            move_coordinates = (move_x, move_y)
            print(f"Camera is pointed at {center_coordinates} but needs to be pointed at {last_detected_location}.")
            print(f"The camera needs moved: {move_coordinates}.")
            if args.track:
                pan(move_x)
                tilt(move_y)

            # Save the image           
            if args.save:
                filename = 'motion-{}.jpg'.format(datetime.now().strftime("%m%d%Y%H%M%S"))
                cv2.imwrite(filename, video_frame)
                cv2.waitKey(0)

            # If there's a Slack token, send a message
            if args.slack_token:
                seconds_since_notified = (datetime.now() - last_notify_time).total_seconds()
                if (seconds_since_notified > args.notification_delay):
                    try:
                        with open(filename, "rb") as image:
                            file = image.read()
                            data = bytearray(file)

                        post_file_to_slack(
                            ':warning: Motion was detected on the Jetson Camera :warning:',
                            args,
                            filename,
                            data)
                        
                        last_notify_time = datetime.now()
                        print(f"Successfully posted notification to Slack: {last_notify_time}")
                    except Exception as e:
                        print(f"Failed to post a notification message: {e}" )
                        continue
                else:
                    if args.debug:
                        print(f"Skipping notification for {args.notification_delay} seconds, we just sent one {seconds_since_notified} seconds ago...")
        else:
            someone_here = False
            if args.debug:
                print(f"[{time}] ...............")

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
    if args.version:
        print(f"Version: {__version__}")

    if args.slack_token:
        print("\n** Slack Notifications: ENABLED **\n")

    if args.debug:
        print("\n** Debug Mode: ENABLED **\n")

    if args.ptz_test:
        print("\n** PTZ Test: ENABLED **\n")

    try:
        if args.ptz_test:
            from pantilt import ptz_demo
            ptz_thread = threading.Thread(target=ptz_demo)
            ptz_thread.daemon = True
            ptz_thread.start()

        process_thread = threading.Thread(target=captureFrames)
        process_thread.daemon = True

        detect_thread = threading.Thread(target=detectMotion)
        detect_thread.daemon = True

        process_thread.start()
        detect_thread.start()

        app.run("0.0.0.0", port=args.port)
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

