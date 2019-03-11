# manual_drive.py

import sys
import os
import tty
import termios
import piplates.MOTORplate as MOTOR
import RPi.GPIO as GPIO
import time
import pdb
from multiprocessing import Process
import Adafruit_LSM303



dummy0=MOTOR.getINTflag1(0)  #flush out any old interrupts
dummy1=MOTOR.getINTflag1(1)  #flush out any old interrupts
#intFLAG=0
#intBITS0=0
#intBITS1=0

#def moveDone(channel):
#        global intBITS0, intBITS1, intFLAG
#        print("motor at steady state")
#        intBITS0=MOTOR.getINTflag1(0)            #get flags
#        intBITS1=MOTOR.getINTflag1(1)            #get flags
#        intFLAG=1       #signal main program that an interrupt occurred


class Motor(object):
    def __init__(self, address, number, forward_direction, reverse_direction, 
            acceleration=0.1):
        if address in [0,1]:
            self._address = address
        else:
            raise ValueError('address must be 0 or 1')
        if number in [1,2,3]:
            self._number = number
        else:
            raise ValueError('number must be 1, 2, or 3')
        if forward_direction in ['cw','ccw'] and reverse_direction in ['cw','ccw']:
            self._forward = forward_direction
            self._reverse = reverse_direction
        else:
            raise ValueError('drections must be "cw" or "ccw"')
        if 0. <= acceleration and acceleration <= 5.:
            self._acceleration = acceleration
        else:
            raise ValueError('acceleration must be between 0. and 5.')

        # set initial motion parameters
        self.direction = self._forward
        self.speed = 0
        self._stopped = True

        # set up interrupts
#        MOTOR.enabledcSTEADYint(self._address, self._number)
#        MOTOR.enabledcSTOPint(self._address, self._number)

        # assign test bits
#        self._testbit = 32 * 2**(5 - self._number)

        


class RuntRover(object):
    """ left side is address 0
        right side is address 1
        wheel 1 is front, wheel 2 is middle, wheel 3 is rear
    """
    MOTOR.intEnable(0) 
    MOTOR.intEnable(1) 

    def __init__(self, min_speed=25):
        # make the motor banks
        self._LEFT = [Motor(0, 1, 'cw', 'ccw'), Motor(0, 2, 'cw', 'ccw'), 
                Motor(0, 3, 'cw', 'ccw')]
        self._RIGHT = [Motor(1, 1, 'ccw', 'cw'), Motor(1, 2, 'ccw', 'cw'), 
                Motor(1, 3, 'ccw', 'cw')]

        # get the motors ready to run
        for m in self._LEFT:
            MOTOR.dcCONFIG(m._address, m._number, m.direction, 0, m._acceleration)
            print("Starting motors at speed 0.")
            MOTOR.dcSTART(m._address, m._number)
            m._stopped = False
        for m in self._RIGHT:
            MOTOR.dcCONFIG(m._address, m._number, m.direction, 0, m._acceleration)
            print("Starting motors at speed 0.")
            MOTOR.dcSTART(m._address, m._number)
            m._stopped = False


    def left(self, increment):
        # decrease speed of left bank
        for m in self._LEFT:
            if m._stopped:
                MOTOR.dcSTART(m._address, m._number)
            tmp = m.speed - increment
            if tmp >= 0 and m.direction == m._forward:
                new_speed = min([tmp, 100])
                MOTOR.dcSPEED(m._address, m._number, new_speed)
                time.sleep(m._acceleration)
                m.speed = new_speed
            elif tmp < 0 and m.direction == m._forward:
                m.direction = m._reverse
                new_speed = min([abs(tmp), 100])
                MOTOR.dcSTOP(m._address, m._number)
                MOTOR.dcCONFIG(m._address, m._number, m.direction, new_speed, m._acceleration)
                MOTOR.dcSTART(m._address, m._number)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            elif tmp < 0 and m.direction == m._reverse:
                new_speed = min([abs(tmp), 100])
                MOTOR.dcSPEED(m._address, m._number, new_speed)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            elif tmp >=0 and m.direction == m._reverse:
                m.direction = m._forward
                new_speed = min([tmp, 100])
                MOTOR.dcSTOP(m._address, m._number)
                MOTOR.dcCONFIG(m._address, m._number, m.direction, new_speed, m._acceleration)
                MOTOR.dcSTART(m._address, m._number)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            print("motor: {0}, {1}    speed: {2}".format(m._address, m._number, m.speed))

        # increase speed of right bank
        for m in self._RIGHT:
            if m._stopped:
                MOTOR.dcSTART(m._address, m._number)
            tmp = m.speed + increment
            if tmp >= 0 and m.direction == m._forward:
                new_speed = min([tmp, 100])
                MOTOR.dcSPEED(m._address, m._number, new_speed)
                time.sleep(m._acceleration)
                m.speed = new_speed
            elif tmp >= 0 and m.direction == m._reverse:
                m.direction = m._forward
                new_speed = min([tmp, 100])
                MOTOR.dcSTOP(m._address, m._number)
                MOTOR.dcCONFIG(m._address, m._number, m.direction, new_speed, m._acceleration)
                MOTOR.dcSTART(m._address, m._number)
                time.sleep(m._acceleration)
                m.speed = new_speed
            elif tmp < 0 and m.direction == m._reverse:
                new_speed = min([abs(tmp), 100])
                MOTOR.dcSPEED(m._address, m._number, new_speed)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            elif tmp < 0 and m.direction == m._forward:
                m.direction = m._reverse
                new_speed = min([abs(tmp), 100])
                MOTOR.dcSTOP(m._address, m._number)
                MOTOR.dcCONFIG(m._address, m._number, m.direction, new_speed, m._acceleration)
                MOTOR.dcSTART(m._address, m._number)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            print("motor: {0}, {1}    speed: {2}".format(m._address, m._number, m.speed))



    def right(self, increment):
        # decrease speed of right bank
        for m in self._RIGHT:
            if m._stopped:
                MOTOR.dcSTART(m._address, m._number)
            tmp = m.speed - increment
            if tmp >= 0 and m.direction == m._forward:
                new_speed = min([tmp, 100])
                MOTOR.dcSPEED(m._address, m._number, new_speed)
                time.sleep(m._acceleration)
                m.speed = new_speed
            elif tmp < 0 and m.direction == m._forward:
                m.direction = m._reverse
                new_speed = min([abs(tmp), 100])
                MOTOR.dcSTOP(m._address, m._number)
                time.sleep(m._acceleration)
                MOTOR.dcCONFIG(m._address, m._number, m.direction, new_speed, m._acceleration)
                MOTOR.dcSTART(m._address, m._number)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            elif tmp < 0 and m.direction == m._reverse:
                new_speed = min([abs(tmp), 100])
                MOTOR.dcSPEED(m._address, m._number, new_speed)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            elif tmp >=0 and m.direction == m._reverse:
                m.direction = m._forward
                new_speed = min([tmp, 100])
                MOTOR.dcSTOP(m._address, m._number)
                time.sleep(m._acceleration)
                MOTOR.dcCONFIG(m._address, m._number, m.direction, new_speed, m._acceleration)
                MOTOR.dcSTART(m._address, m._number)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            print("motor: {0}, {1}    speed: {2}".format(m._address, m._number, m.speed))

        # increase speed of left bank
        for m in self._LEFT:
            if m._stopped:
                MOTOR.dcSTART(m._address, m._number)
            tmp = m.speed + increment
            if tmp >= 0 and m.direction == m._forward:
                new_speed = min([tmp, 100])
                MOTOR.dcSPEED(m._address, m._number, new_speed)
                time.sleep(m._acceleration)
                m.speed = new_speed
            elif tmp >= 0 and m.direction == m._reverse:
                m.direction = m._forward
                new_speed = min([tmp, 100])
                MOTOR.dcSTOP(m._address, m._number)
                time.sleep(m._acceleration)
                MOTOR.dcCONFIG(m._address, m._number, m.direction, new_speed, m._acceleration)
                MOTOR.dcSTART(m._address, m._number)
                time.sleep(m._acceleration)
                m.speed = new_speed
            elif tmp < 0 and m.direction == m._reverse:
                new_speed = min([abs(tmp), 100])
                MOTOR.dcSPEED(m._address, m._number, new_speed)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            elif tmp < 0 and m.direction == m._forward:
                m.direction = m._reverse
                new_speed = min([abs(tmp), 100])
                MOTOR.dcSTOP(m._address, m._number)
                time.sleep(m._acceleration)
                MOTOR.dcCONFIG(m._address, m._number, m.direction, new_speed, m._acceleration)
                MOTOR.dcSTART(m._address, m._number)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            print("motor: {0}, {1}    speed: {2}".format(m._address, m._number, m.speed))


    def forward(self, increment):
        # increase forward speed of both banks
        for m in self._LEFT + self._RIGHT:
            if m._stopped:
                MOTOR.dcSTART(m._address, m._number)
            tmp = m.speed + increment
            if tmp >= 0 and m.direction == m._forward:
                new_speed = min([100, tmp])
                MOTOR.dcSPEED(m._address, m._number, new_speed)
                time.sleep(m._acceleration)
                m.speed = new_speed
            if tmp >= 0 and m.direction == m._reverse:
                m.direction = m._forward
                new_speed = min([100, tmp])
                MOTOR.dcSTOP(m._address, m._number)
                time.sleep(m._acceleration)
                MOTOR.dcCONFIG(m._address, m._number, m.direction, new_speed, m._acceleration)
                MOTOR.dcSTART(m._address, m._number)
                time.sleep(m._acceleration)
                m.speed = new_speed
            if tmp < 0 and m.direction == m._forward:
                m.direction = m._reverse
                new_speed = min([100, abs(tmp)])
                MOTOR.dcSTOP(m._address, m._number)
                time.sleep(m._acceleration)
                MOTOR.dcCONFIG(m._address, m._number, m.direction, new_speed, m._acceleration)
                MOTOR.dcSTART(m._address, m._number)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            if tmp < 0 and m.direction == m._reverse:
                new_speed = min([100, abs(tmp)])
                MOTOR.dcSPEED(m._address, m._number, new_speed)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            print("motor: {0}, {1}    speed: {2}".format(m._address, m._number, m.speed))


    def reverse(self, increment):
        # decrease forward speed of both banks
        for m in self._LEFT + self._RIGHT:
            if m._stopped:
                MOTOR.dcSTART(m._address, m._number)
            tmp = m.speed - increment
            if tmp >= 0 and m.direction == m._forward:
                new_speed = min([100, tmp])
                MOTOR.dcSPEED(m._address, m._number, new_speed)
                time.sleep(m._acceleration)
                m.speed = new_speed
            if tmp >= 0 and m.direction == m._reverse:
                m.direction = m._forward
                new_speed = min([100, tmp])
                MOTOR.dcSTOP(m._address, m._number)
                time.sleep(m._acceleration)
                MOTOR.dcCONFIG(m._address, m._number, m.direction, new_speed, m._acceleration)
                MOTOR.dcSTART(m._address, m._number)
                time.sleep(m._acceleration)
                m.speed = new_speed
            if tmp < 0 and m.direction == m._forward:
                m.direction = m._reverse
                new_speed = min([100, abs(tmp)])
                MOTOR.dcSTOP(m._address, m._number)
                time.sleep(m._acceleration)
                MOTOR.dcCONFIG(m._address, m._number, m.direction, new_speed, m._acceleration)
                MOTOR.dcSTART(m._address, m._number)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            if tmp < 0 and m.direction == m._reverse:
                new_speed = min([100, abs(tmp)])
                MOTOR.dcSPEED(m._address, m._number, new_speed)
                time.sleep(m._acceleration)
                m.speed = -new_speed
            print("motor: {0}, {1}    speed: {2}".format(m._address, m._number, m.speed))


    def stop(self):
        for m in self._LEFT + self._RIGHT:
            MOTOR.dcSTOP(m._address, m._number)
            time.sleep(m._acceleration)
            m.speed = 0
            m._direction = m._forward
            MOTOR.dcCONFIG(m._address, m._number, m.direction, m.speed, m._acceleration)
            m._stopped = True
            print("motor: {0}, {1}    speed: {2}".format(m._address, m._number, m.speed))


class Controller(object):
    def __init__(self, increment=10, video=False, test_modules = None):
        self._robot = RuntRover()
        self._increment = increment
        self._run = False
        if test_modules is not None:
            self._test_modules = test_modules

    def start(self):
        try:
            self._run = True
            while self._run:
                cmd = self.getck()
                if cmd == 'SPACE':
                    self._robot.stop()
                if cmd == 'FORWARD':
                    self._robot.forward(self._increment)
                if cmd == 'BACKWARD':
                    self._robot.reverse(self._increment)
                if cmd == 'LEFTWARD':
                    self._robot.left(self._increment)
                if cmd == 'RIGHTWARD':
                    self._robot.right(self._increment)
                for test in self._test_modules:
                    test_modules.execute()

        except KeyboardInterrupt:
            self._robot.stop()
            self.cleanup()

        except:
            self._robot.stop()
            self.cleanup()

        finally:
            self._robot.stop()
            self.cleanup()

    def stop(self):
        pass

    def cleanup(self):
        self._run = False

    def getck(self):
        """ Returns motion command based on control key press."""
        fd = sys.stdin.fileno()
        orig_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(sys.stdin.fileno())
            tpl = []
            while(True):
                ch = sys.stdin.read(1)
                if ch=='q':
                    self.cleanup()
                    break
                if ch==' ':
                    return 'SPACE'
                if not ch=='':
                    tpl.append(ch)
                if not tpl[0] == '\x1b':
                    # not an escaped character, so ignore
                    tpl = []
                elif len(tpl) == 3:
                    tpl = ''.join(tpl)
                    if tpl=='\x1b[A':
                            return 'FORWARD'
                    elif tpl=='\x1b[B':
                            return 'BACKWARD'
                    elif tpl=='\x1b[C':
                            return 'RIGHTWARD'
                    elif tpl=='\x1b[D':
                            return 'LEFTWARD'
                    else:
                        tpl = []
        except KeyboardInterrupt:
            print("terminated by user... cleaning up")
            self.cleanup()
        except:
            self.cleanup()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, orig_settings)


def main():
    #threading/queue goes here
#    c = Controller()
    c = Controller(test_modules=[tiltSwitch()])
    c.start()


class tiltSwitch(object):
    def __init__(self):
        self._lsm303 = Adafruit_LSM303.LSM303()
        self._robot = RuntRover()
    
    def execute():

        while (True):
            accel = self._lsm303.read()
            accel_x, accel_y, accel_z = accel

                #if(accel_x > ?):
                #self._robot.stop()
        
            if (accel_x < -650):
                print("backing up")
        
            if (accel_y < -550):
                print("left tilt")
        
            if (accel_y > 475):
                print("right tilt")

def monitor():
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
    
        if key == ord("q"):
            break

if __name__=='__main__':
        video = False
        args = sys.argv
        if len(args)> 1:
            if args[1] == 'video':
                video = True
        if video:
            mon_proc = Process(target = monitor)
#            main_proc = Process(target = main)
            mon_proc.start()
#            main_proc.start()
            main()
        else:
            main()
