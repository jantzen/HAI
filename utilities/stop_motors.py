from BBR.nodes.actuators.DCmotor_MOTORplate import *

# create the motor objects
motors1 = []
motors2 = []
for ii in range(3):
    motors1.append(MPMotor([], 0, ii+1, 'cw', 
        'ccw'))
for ii in range(3):
    motors2.append(MPMotor([], 1, ii+1, 'ccw', 
        'cw'))

# stop the motors
for m in motors1:
    m.stop()
for m in motors2:
    m.stop()
