import threading
import time
import random
import atexit
import picamera
import Adafruit_LSM303
from bot import Bot

bot = Bot()

class wander(threading.Thread):
    #def __init__(self):

    def run(self):
        self.stop_event = threading.Event()
        commands = ['forward', 'right', 'left']
        while (not self.stop_event.is_set()):
            self.command = random.choice(commands)
            #command(random.choice(commands))
            self.stop_event.wait(random.uniform(0,3))

    def stop(self):
        self.stop_event.set()


class balance_reflex(threading.Thread):
    #def __init__(self):

    def run(self):
        lsm303 = Adafruit_LSM303.LSM303()
        self.stop_event = threading.Event()
        while (not self.stop_event.is_set()):
            accel, mag = lsm303.read()
            accel_x, accel_y, accel_z = accel
            mag_x, mag_z, mag_y = mag
            #note different order of axes
            #do something with the results of the accelerometer read
            #if tilted too far, backup otherwise do nothing
            #also need to control for noise, for now just set the limits very conservatively
            if accel_x > 450:
                self.command = 'back'
            else:
                self.command = ''
            #backup will need to override the wander module
            time.sleep(0.5)

def command(message):
    if message == 'forward':
        bot.move(40)
    if message == 'left' OR message == 'right':
        bot.movingTurn(message, 40)
    if message == 'back':
        bot.move(35, true)

thread1 = wander()
thread1.start()
thread2 = balance_reflex()
thread2.start()

while(1):
    if thread2.command:
        command(thread2.command)
    elif thread1.command:
        command(thread1.command)
    time.sleep(0.1)

#kill modules on exiting main program
def killModules():
    thread1.stop()
    thread2.stop()
atexit.register(killModules)