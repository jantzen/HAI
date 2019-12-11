# file: test_dual_FSR_strip.py

from BBR.nodes.sensors.dual_FSR_strip import *
import multiprocessing as mp
import queue
import time


def test_dual_FSR_strip():
    # set up a queue to catch output
    q = mp.Queue(maxsize=6)

    # create a sensor object
    fsr = Dual_FSR_strips([q])

    # launch a sensor process
    p = mp.Process(target=fsr.run)
    p.start()

    # interact with sensor
    start = time.time()
    print("Touch the  front sensor 3 times, then the rear.")
    time.sleep(10.)

    # check results
    assert q.qsize() == 6

    # cleanup
    p.terminate()
    p.join()

