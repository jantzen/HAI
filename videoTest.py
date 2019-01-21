from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    hsv = cv2.cvtColor(frame.array, cv2.COLOR_BGR2HSV)
    
    lower_green = np.array([90, 50, 50])
    upper_green = np.array([115, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    masked = cv2.bitwise_and(frame.array, frame.array, mask = mask)
    
    contours,hr = cv2.findContours(mask,1,2)
    
    if len(contours) != 0:
        cv2.drawContours(masked, contours, -1, 255, 3)
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(masked,(x,y),(x+w,y+h),(0,255,0),2)
        xCenter = ((x + (x+w))/2)
    
    #for c in contours:
        #approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
        #if len(approx) > 15:
            #cv2.drawContours(edges,[c],0,(255,255,0),-1)
    
    cv2.imshow("Original", frame.array)
    cv2.imshow("Color Match", masked)
    #cv2.imshow("Center", xCenter)
    #cv2.imshow("Mask", mask)
    #cv2.imshow("Threshold", thresh)
    #cv2.imshow("Dilation", dilation)
    #cv2.imshow("Gray", gray)
    #cv2.imshow("Iso", edges)
    key = cv2.waitKey(1) & 0xFF
    
    rawCapture.truncate(0)

    time.sleep(1.0)

    if key == ord("q"):
        break
