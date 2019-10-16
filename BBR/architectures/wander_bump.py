"""Implemnts a simple wander-and-bump subsumption architecture on a platform using:
    (list equipment)
"""
from BBR.nodes.sensors.dual_FSR_strip import Dual_FSR_strips
from BBR.nodes.internodes.bump import Bump
from BBR.nodes.internodes.wander import Wander
from BBR.nodes.actuators.DCmotor_MOTORplate import MPMotor, RuntRoverSide
import multiprocessing as mp
import time


def main():
    # set up queues for sensors and internodes
    print("Setting up queues...")
    q12 = mp.Queue(maxsize=1)
    q24 = mp.Queue(maxsize=1)
    q25 = mp.Queue(maxsize=1)
    q34 = mp.Queue(maxsize=1)
    q35 = mp.Queue(maxsize=1)
    qw = mp.Queue(maxsize=1)
    qfsr = mp.Queue(maxsize=1)

    # set up sensor nodes and internodes
    print("Setting up nodes and internodes...")
    fsr = Dual_FSR_strips(afferents=[qfsr], efferents=[q12])
    b = Bump(afferents=[q12], efferents=[q24, q25])
    w = Wander(afferents=[qw], efferents=[q34, q35])

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
            reverse_direction='ccw', max_run_speed=50))
    motors_right = []
    for ii, mq in enumerate(mq_right):
        motors_right.append(MPMotor([mq], 1, ii+1, forward_direction='ccw', 
            reverse_direction='cw', max_run_speed=50))

    # create the RuntRoverSide objects
    print("Creating RuntRoverSide objects...")
    rr_left = RuntRoverSide(0, [q24, q34], mq_left)
    rr_right = RuntRoverSide(1, [q25, q35], mq_right)

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
    time.sleep(0.1)
    proc_b.start()
    time.sleep(0.1)
    for p in procs_m_left:
        p.start()
        time.sleep(0.1)
    for p in procs_m_right:
        p.start()
        time.sleep(0.1)
    proc_rr_left.start()
    time.sleep(0.1)
    proc_rr_right.start()
    time.sleep(0.1)
    proc_w.start()
    time.sleep(0.1)

    # put main process into a loop
    run = True
    print("Robot running.")
    while run:
        try:
            tmp = input("Press q to quit.\n")
            if not tmp == 'q':
                print("invalid input")
            elif tmp == 'q':

                # quit and join all processes
                print("User terminated process...")
               
                print("Signaling all running nodes to quit:")
                if proc_w.is_alive():
                    qw.put('q') 
                if proc_fsr.is_alive():
                    qfsr.put('q')
                time.sleep(5.)


                print("Joining...")
                print("...fsr join...")
                proc_fsr.join()
                print("...bump join...")
                proc_b.join()
                print("...left motor procs join...")
                for p in procs_m_left:
                    p.join()
                print("...right motor procs join...")
                for p in procs_m_right:
                    p.join()
                print("...left rr join...")
                proc_rr_left.join()
                print("...right rr join...")
                proc_rr_right.join()
                print("...wander join...")
                proc_w.join()
                run = False

        except KeyboardInterrupt:
            print("Signaling all running nodes to quit:")
            if proc_w.is_alive():
                qw.put('q') 
            if proc_fsr.is_alive():
                qfsr.put('q')
            time.sleep(5.)


            print("Joining...")
            proc_fsr.join()
            proc_b.join()
            for p in procs_m_left:
                p.join()
            for p in procs_m_right:
                p.join()
            proc_rr_left.join()
            proc_rr_right.join()
            proc_w.join()
            proc_listen.joint()
            run = False


if __name__ == "__main__":
    main()
