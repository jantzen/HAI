#import piplates.MOTORplate as MOTO
#import time
#
#FORWARD = [['cw','cw','cw'],['ccw','ccw','ccw']]
#REVERSE = [['ccw','ccw','ccw'],['cw','cw','cw']]
#
#for i in range(1,4):
#    MOTO.dcCONFIG(0, i, FORWARD[0][i-1], 50, 1)
#    MOTO.dcCONFIG(1, i, FORWARD[1][i-1], 50, 1)
#
#for i in range(2):
#    for j in range(1,4):
#        MOTO.dcSTART(i,j)
#
#time.sleep(2.5)
#
#for i in range(2):
#    for j in range(1,4):
#        MOTO.dcSTOP(i,j)
#
#time.sleep(1.)
#
#for i in range(1,4):
#    MOTO.dcCONFIG(0, i, REVERSE[0][i-1], 50, 1)
#    MOTO.dcCONFIG(1, i, REVERSE[1][i-1], 50, 1)
#
#for i in range(2):
#    for j in range(1,4):
#        MOTO.dcSTART(i,j)
#
#time.sleep(2.5)
#
#for i in range(2):
#    for j in range(1,4):
#        MOTO.dcSTOP(i,j)
#


# getck method based partly on code from
# https://stackoverflow.com/questions/22397289/finding-the-values-of-the-arrow-keys-in-python-why-are-they-triples

import sys
import tty
import termios
import piplates.MOTORplate as MOTOR
import RPi.GPIO as GPIO
import time
import pdb

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
            print("left speed: {}".format(m.speed))

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
            print("right speed: {}".format(m.speed))



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
            print("right speed: {}".format(m.speed))

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
            print("left speed: {}".format(m.speed))


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
            print(m.speed)


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
            print(m.speed)


    def stop(self):
        for m in self._LEFT + self._RIGHT:
            MOTOR.dcSTOP(m._address, m._number)
            m.speed = 0
            m._direction = m._forward
            m._stopped = True


def closeout():
    GPIO.cleanup()


def getck():
    """ Returns motion command based on control key press."""
    fd = sys.stdin.fileno()
    orig_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(sys.stdin.fileno())
        tpl = []
        while(True):
            ch = sys.stdin.read(1)
            if ch=='q':
                closeout()
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
                    print('not an arrow key')
                    tpl = []
    except KeyboardInterrupt:
        print("terminated by user... cleaning up")
    except:
        closeout()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, orig_settings)


def main():
    out = getck()
    print(out)



if __name__=='__main__':
        main()
