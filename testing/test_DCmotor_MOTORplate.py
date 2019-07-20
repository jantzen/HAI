from BBR.nodes.actuators.DCmotor_MOTORplate import *
import multiprocessing as mp
import time

def test_MPMotor(address=0, number=1, forward_direction='cw', reverse_direction='ccw'):
    # create queue for afferent
    q = mp.Queue(maxsize=1)

    # create the motor object
    m = MPMotor([q], address, number, forward_direction, reverse_direction)

    # spawn the motor process
    print("Starting motor process...")
    p = mp.Process(target=m.run)
    p.start()

    # add a series of commands to the afferent queue
    for ii in range(15):
        q.put('f')
        time.sleep(0.1)

    time.sleep(1.0)

    for ii in range(15):
        q.put('r')
        time.sleep(0.1)

    time.sleep(0.1)

    q.put('s')

    time.sleep(1.0)

    for ii in range(15):
        q.put('r')
        time.sleep(0.1)

    for ii in range(15):
        q.put('f')
        time.sleep(0.1)

    time.sleep(0.1)

    q.put('s')

    time.sleep(0.1)

    q.put('q')

    time.sleep(0.1)

    p.join()

