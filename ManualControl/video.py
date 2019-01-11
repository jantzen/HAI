# video.py

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    cv2.imshow("Live", frame.array)

    rawCapture.truncate(0)

    key = cv2.waitKey(1) & 0xFF

#    time.sleep(0.01)

    if key == ord("q"):
        break
