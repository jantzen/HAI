import piplates.MOTORplate as MOTOR

#print MOTOR.Poll()

MOTOR.RESET(0)
MOTOR.RESET(1)

#left is plate addr 0, right is plate addr 1
#front wheel is motor 1, back wheel is motor 3

class Motorset:
    def __init__(self, side):
        self.running = False
        self.side = side
        if side == 'left':
            self.plate = 1
            self.forward = 'ccw'
            self.backward = 'cw'
        if side == 'right':
            self.plate = 0
            self.forward = 'cw'
            self.backward = 'ccw'

    def motorStart(self, plate, motor, dir, speed, accel):
        MOTOR.dcCONFIG(self.plate, motor, dir, speed, accel)
        MOTOR.dcSTART(self.plate, motor)

    def motorChange(self, plate, motor, speed):
        MOTOR.dcSPEED(plate, motor, speed)

    def motorStop(self, plate, motor):
        MOTOR.dcSTOP(plate, motor)

    def moveOne(self, motor, speed, backward=False, accel=.5):
        if backward:
            dir = self.forward
        else:
            dir = self.backward
        if self.running:
            self.motorChange(self.plate, motor, speed)
        else:
            self.motorStart(self.plate, motor, speed, accel)
            self.running = True

    def moveAll(self, speed, backward=False, accel=.5):
        if backward:
            dir = self.forward
        else:
            dir = self.backward
        if self.running:
            for x in range(1, 4):
                self.motorChange(self.plate, x, speed)
        else:
            for x in range(1, 4):
                self.motorStart(self.plate, x, dir, speed, accel)
            self.running = True

    def stopAll(self):
        for x in range(1, 4):
            self.motorStop(self.plate, x)
        self.running = False

    def emergencyStopAll(self):
        #this one still needs work
        for x in range(1, 4):
            MOTOR.dcCONFIG(self.plate, x, 'cw', 0, 0)
            self.motorStop(self.plate, x)
        self.running = False

class Bot:
    def __init__(self):
        self.right = Motorset('right')
        self.left = Motorset('left')

    def move(self, spd, back=False, accel=.5):
        self.right.moveAll(spd, back, accel)
        self.left.moveAll(spd, back, accel)

    def movingTurn(self, dir, spd):
        #side of the direction of turn moves a bit slower
        if dir == right:
            self.right.moveAll(spd-20)
            self.left.moveAll(spd)
        if dir == left:
            self.right.moveAll(spd)
            sefl.left.moveAll(spd-20)

    def turn(self, dir, spd):
        #turn in place
        #change direction commands while motors are running are ignored
        self.stopAll()
        
        if dir == 'right':
            self.right.moveAll(spd, True)
            self.left.moveAll(spd)
        if dir == 'left':
            self.right.moveAll(spd)
            self.left.moveAll(spd, True)

    def stopAll(self):
        self.right.stopAll()
        self.left.stopAll()

    def emergencyStopAll(self):
        self.right.emergencyStopAll()
        self.left.emergencyStopAll()
