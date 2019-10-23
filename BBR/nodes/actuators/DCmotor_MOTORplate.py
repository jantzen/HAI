from BBR.nodes.actuators.DCmotor import *
import piplates.MOTORplate as MOTORplate
import multiprocessing 
import time
import queue # piplates requires Python 2.7

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
        self.direction = self._forward
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

    def __init__(self, ident, afferents, motor_queues, efferents=None):
        if not (type(motor_queues) is list):
            raise ValueError('must provide a list of lists of motor_queues')
        MotorCluster.__init__(self, afferents, efferents)
        self._motor_queues = motor_queues
        self.ident = ident


    def start(self):
        for m in self._motor_queues:
            m.put('a')
            time.sleep(0.1)


    def stop(self):
        for m in self._motor_queues:
            m.put('s')
            time.sleep(0.1)


    def forward(self):
        for m in self._motor_queues:
            m.put('f')
            time.sleep(0.1)


    def reverse(self):
        for m in self._motor_queues:
            m.put('r')
            time.sleep(0.1)


    def quit(self):
        print("RuntRoverSide node quitting")
        self._run = False
        for m in self._motor_queues:
            m.put('q')
            time.sleep(0.1)


    def run(self):
        while self._run:
            try:
                cmd = None
                for aff in self._afferents:
                    if not aff.empty():
                        cmd = aff.get()
                        break
                if not cmd == None:
                    print("RuntRoverSide {0} received command {1}".format(self.ident, cmd))
                if cmd == 'a':
                    self.start()
                elif cmd == 's':
                    self.stop()
                elif cmd == 'f':
                    self.forward()
                elif cmd == 'r':
                    self.reverse()
                elif cmd == 'q':
                    self.quit()
            except queue.Empty:
                print("queue empty")
                continue
            except KeyboardInterrupt:
                print("RunRoverSide node received keyboard interrupt...")
                self._run = False
                self.quit()
                self.cleanup()
            except:
                self._run = False
                self.quit()
                self.cleanup()


#    def terminate(self, signum, frame):
#        print("terminating RuntRoverSide node process with signum={}".format(signum))
#        self._run = False
#        self.quit()
 


#class RuntRover( MotorSystem ):
#    pass
