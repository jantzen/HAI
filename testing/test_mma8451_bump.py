# file: test_mma8451_bump.py

from BBR.nodes.sensors.mma8451_bump import *
import multiprocessing as mp
import queue
import time

def test_read():
    # create a sensor object
    mma = mma8451_bump([],[])

    out = mma.read()

    assert out is None


def test_quit():
    # create an afferent queue
    aff = mp.Queue(maxsize=1)
    aff.put('q')

    # create a sensor object
    mma = mma8451_bump([aff],[])

    p = mp.Process(target=mma.run)
    p.start()
    time.sleep(1.)
    p.join()

    assert aff.qsize() == 0
    

def test_mma8451_bump():
    # set up a queue to catch output
    aff = mp.Queue(maxsize=1)
    eff = mp.Queue()

    # create a sensor object
    mma = mma8451_bump([aff],[eff])

    # launch a sensor process
    p = mp.Process(target=mma.run)
    p.start()

    # interact with sensor
    start = time.time()
    print("Tap the  front bumper once, then the rear once.")
    time.sleep(10.)
    
    # shut down the node
    aff.put('q')
    time.sleep(0.5)

    # check results
    print(eff.qsize())
    assert eff.qsize() >= 3
    while not eff.empty():
        print(eff.get())

    # cleanup
    p.join()

