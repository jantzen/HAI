from BBR.nodes.actuators.DCmotor import *
import piplates.MOTORplate as MP

class MPMotor( Motor ):    
    
    def __init__(self, afferents, address, number, forward_direction, reverse_direction, 
            acceleration=0.1):

        Motor.__init__(self, afferents=afferents)

        if address in [0,1]:
            self._address = address
        else:
            raise ValueError('address must be 0 or 1')
        if number in [1,2,3,4]:
            self._number = number
        else:
            raise ValueError('number must be 1, 2, 3, or 4')
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

    def start(self):
        pass

    def run():
        pass


class RuntRoverSide( MotorCluster ):
    """Provides a simple interface for controlling the three motors on one side
    of the Runt Rover chassis.
    """

    def __init__(self, afferents, addresses, forward_directions,
            reverse_directions, motor_list):
        Motor.__init__(self, afferents)
        self._motor_list = motor_list
        self._address = addresses # board address for each motor
        self._forward_directions = forward_directions
        self._reverse_directions = reverse_directions

        # set up the motor objects
        self._motors = []
        for ii, motorid in motor_list:
            self._motors.append(MPmotor(None, self._addresses[ii],
                ii, self._forward_directions[ii], self.reverse_directions[ii]))

    def increase(self, increment=10):
        pass

    def decrease(self, increment=10):
        pass


    def run():
        pass

class RuntRover( MotorSystem ):
    pass
