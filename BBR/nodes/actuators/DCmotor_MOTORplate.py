from BBR.nodes.actuators.DCmotor import *
import piplates.MOTORplate as MOTORplate
import multiprocessing 
import time
import Queue # piplates requires Python 2.7
import pdb

class MPMotor( Motor ):    
    
    def __init__(self, afferents, address, number, forward_direction, reverse_direction,
            min_run_speed=20, max_run_speed=90, increment=5, acceleration=0.1):

        Motor.__init__(self, afferents=afferents)

        self._address = address
        if number in [1, 2, 3, 4]:
            self._number = number
        else:
            raise ValueError('motor number must be 1 - 4')
        if forward_direction in ['cw','ccw'] and reverse_direction in ['cw','ccw']:
            self._forward = forward_direction
            self._reverse = reverse_direction
        else:
            raise ValueError('drections must be "cw" or "ccw"')
        if 0 <= min_run_speed <= 100 and 0 <= max_run_speed <= 100 and min_run_speed < max_run_speed:
            self._min_run_speed = min_run_speed
            self._max_run_speed = max_run_speed
        else:
            raise ValueError('min_run_speed must be less and then max_run_speed and both speeds must be in the interval 0 to 100')
        if increment <= (max_run_speed - min_run_speed):
            self._increment = increment
        else:
            raise ValueError('increment too large')
        if 0. <= acceleration and acceleration <= 5.:
            self._acceleration = acceleration
        else:
            raise ValueError('acceleration must be between 0. and 5.')

        # set initial motion parameters
        self.direction = self._forward
        self.speed = 0
        self._stopped = True

        # get the motor ready to run
        MOTORplate.dcCONFIG(self._address, self._number, self.direction, 0, self._acceleration)
 

    def start(self):
        print("Starting motor {} at speed {}.".format(self._number, self.speed))
        MOTORplate.dcSTART(self._address, self._number)
        self._stopped = False


    def stop(self):
        MOTORplate.dcSTOP(self._address, self._number)
        time.sleep(self._acceleration)
        self.speed = 0
        self._direction = self._forward
        MOTORplate.dcCONFIG(self._address, self._number, self.direction, self.speed, self._acceleration)
        self._stopped = True
 

    def forward(self):
        if self._stopped:
            MOTORplate.dcSTART(self._address, self._number)
            self._stopped = False
        tmp = self.speed + self._increment
        if tmp >= 0 and self.direction == self._forward:
            new_speed = min([self._max_run_speed, tmp])
            MOTORplate.dcSPEED(self._address, self._number, new_speed)
            time.sleep(self._acceleration)
            self.speed = new_speed
        if tmp >= 0 and self.direction == self._reverse:
            self.direction = self._forward
            new_speed = min([self._max_run_speed, tmp])
            MOTORplate.dcSTOP(self._address, self._number)
            time.sleep(self._acceleration)
            MOTORplate.dcCONFIG(self._address, self._number, self.direction, new_speed, self._acceleration)
            MOTORplate.dcSTART(self._address, self._number)
            time.sleep(self._acceleration)
            self.speed = new_speed
        if tmp < 0 and self.direction == self._forward:
            self.direction = self._reverse
            new_speed = min([self._max_run_speed, abs(tmp)])
            MOTORplate.dcSTOP(self._address, self._number)
            time.sleep(self._acceleration)
            MOTORplate.dcCONFIG(self._address, self._number, self.direction, new_speed, self._acceleration)
            MOTORplate.dcSTART(self._address, self._number)
            time.sleep(self._acceleration)
            self.speed = -new_speed
        if tmp < 0 and self.direction == self._reverse:
            new_speed = min([self._max_run_speed, abs(tmp)])
            MOTORplate.dcSPEED(self._address, self._number, new_speed)
            time.sleep(self._acceleration)
            self.speed = -new_speed


    def reverse(self):
        if self._stopped:
            MOTORplate.dcSTART(self._address, self._number)
            self._stopped = False
        tmp = self.speed - self._increment
        if tmp >= 0 and self.direction == self._forward:
            new_speed = min([self._max_run_speed, tmp])
            MOTORplate.dcSPEED(self._address, self._number, new_speed)
            time.sleep(self._acceleration)
            self.speed = new_speed
        if tmp >= 0 and self.direction == self._reverse:
            self.direction = self._forward
            new_speed = min([self._max_run_speed, tmp])
            MOTORplate.dcSTOP(self._address, self._number)
            time.sleep(self._acceleration)
            MOTORplate.dcCONFIG(self._address, self._number, self.direction, new_speed, self._acceleration)
            MOTORplate.dcSTART(self._address, self._number)
            time.sleep(self._acceleration)
            self.speed = new_speed
        if tmp < 0 and self.direction == self._forward:
            self.direction = self._reverse
            new_speed = min([self._max_run_speed, abs(tmp)])
            MOTORplate.dcSTOP(self._address, self._number)
            time.sleep(self._acceleration)
            MOTORplate.dcCONFIG(self._address, self._number, self.direction, new_speed, self._acceleration)
            MOTORplate.dcSTART(self._address, self._number)
            time.sleep(self._acceleration)
            self.speed = -new_speed
        if tmp < 0 and self.direction == self._reverse:
            new_speed = min([self._max_run_speed, abs(tmp)])
            MOTORplate.dcSPEED(self._address, self._number, new_speed)
            time.sleep(self._acceleration)
            self.speed = -new_speed
 

class RuntRoverSide( MotorCluster ):
    """Provides a simple interface for controlling the three motors on one side
    of the Runt Rover chassis.
    """

    def __init__(self, afferents, addresses, forward_directions,
            reverse_directions, motor_list, min_run_speed=20, max_run_speed=90, increment=5, acceleration=0.1):
        if not (len(addresses) == len(forward_directions) and 
                len(forward_directions) == len(reverse_directions) and 
                len(reverse_directions) == len(motor_list)):
            raise ValueError('must provide addresses and directions for each motor in motor_list')
        MotorCluster.__init__(self, afferents, motor_list)
        self._motor_list = motor_list
        self._addresses = addresses # board address for each motor
        self._forward_directions = forward_directions
        self._reverse_directions = reverse_directions
        self._min_run_speed = min_run_speed
        self._max_run_speed = max_run_speed
        self._increment = increment
        self._acceleration = acceleration

        # set up queues for motor objects
        motor_queues = []
        for m in motor_list:
            motor_queues.append(multiprocessing.Queue(maxsize=1))

        # set up the motor objects
        self._motors = []
        for ii, motorid in enumerate(motor_list):
            self._motors.append(MPMotor([motor_queues[ii]], self._addresses[ii],
                motorid, self._forward_directions[ii], self._reverse_directions[ii],
                self._min_run_speed, self._max_run_speed, self._increment,
                self._acceleration))


    def start(self):
        for m in self._motors:
            m.start()


    def stop(self):
        for m in self._motors:
            m._afferents[0].put('s')


    def forward(self):
        for m in self._motors:
            m._afferents[0].put('f')


    def reverse(self):
        for m in self._motors:
            m._afferents[0].put('r')


    def run(self):
        while True:
            try:
                cmd = None
                for aff in self._afferents:
                    if not aff.empty():
                        cmd = aff.get()
                        print("command received")
                        break
                if cmd == 's':
                    self.stop()
                elif cmd == 'f':
                    self.forward()
                elif cmd == 'r':
                    self.reverse()
            except Queue.Empty:
                print("queue empty")
                continue

        sys.exit(0)
 


class RuntRover( MotorSystem ):
    pass
