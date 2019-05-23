import piplates.MOTORplate as MOTOR
import RPi.GPIO as GPIO
import time


isActivated = False

if (isActivated == True):
    print("button press worked!")

#Use pin numbers
GPIO.setmode(GPIO.BOARD)

#sets up the pins
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.IN)

#input channel pin 12
input_channel = GPIO.input(12)

#output channel pin 11
output_channel = GPIO.output(11, false)


#add event that tracks rising change in rate of electrical signal to input channel
GPIO.add_event_detect(12, GPIO.RISING)
    
if GPIO.event_detected(12):
    isActivated = True
    time.sleep(1)
