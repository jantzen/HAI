import DCmotors
import piplates.MOTORplate as MOTOR

class Motor( DCmotors.Motor ):    
    
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

