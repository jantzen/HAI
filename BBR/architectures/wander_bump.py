"""Implemnts a simple wander-and-bump subsumption architecture on a platform using:
    (list equipment)
"""
from BBR.nodes.sensors.dual_FSR_strip import Dual_FSR_strips
from BBR.nodes.internodes.bump import Bump
from BBR.nodes.internodes.wander import Wander
from BBR.nodes.actuators.DCmotor_MOTORplate import MPMotor, RuntRoverSide
import multiprocessing as mp
import sys
import time


def main():
    # set up queues for sensors and internodes
    print("Setting up queues...")
    q12 = mp.Queue(maxsize=1)
    q24 = mp.Queue(maxsize=1)
    q25 = mp.Queue(maxsize=1)
    q34 = mp.Queue(maxsize=1)
    q35 = mp.Queue(maxsize=1)

    # set up sensor nodes and internodes
    print("Setting up nodes and internodes...")
    fsr = Dual_FSR_strips(efferents=[q12])
    b = Bump(afferents=[q12], efferents=[q24, q25])
    w = Wander(efferents=[q34, q35])

    # set up queues for motor afferents
    print("Setting up queues for motor afferents...")
    mq_left = []
    for ii in range(3):
        mq_left.append(mp.Queue(maxsize=1))
    mq_right = []
    for ii in range(3):
        mq_right.append(mp.Queue(maxsize=1))

    # create the motor objects
    print("Creating the motor objects...")
    motors_left = []
    for ii, mq in enumerate(mq_left):
        motors_left.append(MPMotor([mq], 0, ii+1, forward_direction='cw', 
            reverse_direction='ccw'))
    motors_right = []
    for ii, mq in enumerate(mq_left):
        motors_right.append(MPMotor([mq], 1, ii+1, forward_direction='ccw', 
            reverse_direction='cw'))

    # create the RuntRoverSide objects
    print("Creating RuntRoverSide objects...")
    rr_left = RuntRoverSide([q24, q34], mq_left)
    rr_right = RuntRoverSide([q25, q35], mq_right)

    # create the processes
    print("Creating and launching node processes...")
    proc_fsr = mp.Process(target=fsr.run)
    proc_b = mp.Process(target=b.run)
    proc_w = mp.Process(target=w.run)
    procs_m_left = []
    for m in motors_left:
        procs_m_left.append(mp.Process(target=m.run))
    procs_m_right = []
    for m in motors_right:
        procs_m_right.append(mp.Process(target=m.run))
    proc_rr_left = mp.Process(target=rr_left.run)
    proc_rr_right = mp.Process(target=rr_right.run)
        
    # launch the processes
    proc_fsr.start()
    time.sleep(0.5)
    proc_b.start()
    time.sleep(0.5)
    proc_w.start()
    time.sleep(0.5)
    for p in procs_m_left:
        p.start()
        time.sleep(0.5)
    for p in procs_m_right:
        p.start()
        time.sleep(0.5)
    proc_rr_left.start()
    time.sleep(0.5)
    proc_rr_right.start()
    time.sleep(0.5)

    # put main process into a loop
    print("Robot running. Press CTRL-C to terminate.")
    while True:
        try:
            time.sleep(0.1)

        except KeyboardInterrupt:
            # terminate and join all processes
            print("User terminated process...")
            proc_fsr.terminate()
            proc_b.terminate()
            proc_w.terminate()
            for p in procs_m_left:
                p.terminate()
            for p in procs_m_right:
                p.terminate()
            proc_rr_left.terminate()
            proc_rr_right.terminate()

            proc_fsr.join()
            proc_b.join()
            proc_w.join()
            for p in procs_m_left:
                p.join()
            for p in procs_m_right:
                p.join()
            proc_rr_left.join()
            proc_rr_right.join()
            sys.exit(0)

if __name__ == "__main__":
    main()
