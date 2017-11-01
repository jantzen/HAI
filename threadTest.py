import threading
import time
import random
import atexit
import picamera
from bot import Bot
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)
#http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-2

def command(message):
    #issue a new standing order from library of bot movements

class wander(threading.Thread):
    #def __init__(self):

    def run(self):
        self.stop_event = threading.Event()
        commands = ['forward', 'right', 'left']
        while (not self.stop_event.is_set()):
            command(random.choice(commands))
            self.stop_event.wait(random.uniform(0,3))

    def stop(self):
        self.stop_event.set()


class reflexes(threading.Thread):
    #def __init__(self):

    def run(self):
        #when sensors indicate problems, generate move commands to avoid
        GPIO.setup()#not sure what all the options here mean
        GPIO.add_event_detect()#this is where callback gets specified

        camera = picamera.PiCamera()
        #how to process camera images in real time without storing anything?

    def callback(self, channel):
        #is this going to get called anytime the sensor's value changes? debounce?



#thread1 = wander()
#thread1.start()

#kill modules on exiting main program
def killModules():
    thread1.stop()
    GPIO.cleanup()
atexit.register(killModules)