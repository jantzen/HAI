from BBR.nodes.actuators.DCmotor_MOTORplate import *
import multiprocessing as mp
import queue
import time


def test_MPMotor(address=0, number=1, forward_direction='cw', reverse_direction='ccw'):

    print("Testing motor {} on board {}".format(number, address))

    # create queue for afferent
    q = mp.Queue(maxsize=1)

    # create the motor object
    m = MPMotor([q], address, number, forward_direction, reverse_direction)

    # spawn the motor process
    print("Starting motor process...")
    p = mp.Process(target=m.run)
    p.start()

    # add a series of commands to the afferent queue
    q.put('a')
    time.sleep(0.1)

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


def test_RuntRoverSide(address=0, forward_direction='cw', reverse_direction='ccw'):

    print("Testing RuntRover side corresponding to board {}".format(address))

    # create queues for motor afferents
    q = []
    for ii in range(3):
        q.append(mp.Queue(maxsize=1))
    
    # create the motor objects
    motors = []
    for ii, mq in enumerate(q):
        motors.append(MPMotor([mq], address, ii+1, forward_direction, 
            reverse_direction))

    # spawn the motor processes
    print("Starting motor processes...")
    m_procs = []
    for m in motors:
        m_procs.append(mp.Process(target=m.run))
    for p in m_procs:
        p.start()

    # create a queue for the RuntRoverSide
    q_rr = mp.Queue(maxsize=1)

    # create the RuntRoverSide
    rr = RuntRoverSide([q_rr], q)

    # spawn RuntRoverSide process
    p_rr = mp.Process(target=rr.run)
    p_rr.start()

    # feed commands to the side
    print("Sending commands to RuntRoverSide...")
    
    q_rr.put('a')
    time.sleep(0.1)

    for ii in range(15):
        q_rr.put('f')
        time.sleep(0.1)

    time.sleep(1.0)

    for ii in range(15):
        q_rr.put('r')
        time.sleep(0.1)

    time.sleep(0.1)

    q_rr.put('s')

    time.sleep(1.0)

    for ii in range(15):
        q_rr.put('r')
        time.sleep(0.1)

    for ii in range(15):
        q_rr.put('f')
        time.sleep(0.1)

    time.sleep(0.1)

    q_rr.put('s')

    time.sleep(0.1)

    q_rr.put('q')

    time.sleep(0.1)

    # set everything down
    for p in m_procs:
        p.join()

    p_rr.join()

