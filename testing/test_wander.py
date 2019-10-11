from BBR.nodes.internodes.wander import *
import multiprocessing as mp
import queue
import time


def helper(q, r):
    while True:
        try:
            if q.empty():
                time.sleep(0.01)
            else:
                r.put(q.get())
        except:
            break
    sys.exit(0)


def test_fire():
    # set up queue as efferent
    q = mp.Queue()

    # set up wander object
    w = Wander([q])

    # trigger the 'fire' method
    w.fire()

    # verify expected output
    out = []
    while not q.empty():
        out.append(q.get())

    assert out == ['f'] * 10 # assumes default burst_size=10


def test_run():
    # set up queue as efferent
    q = mp.Queue()

    # set up queue to collect output
    r = mp.Queue()

    # set up wander object
    w = Wander([q])

    # launch wander and helper processes
    p_wander = mp.Process(target=w.run)
    p_helper = mp.Process(target=helper, args=(q,r))
    p_wander.start()
    p_helper.start()
    
    # wait for output to accumulate
    print("Please wait 10 seconds...")
    time.sleep(10.)

    # stop processes
    p_wander.terminate()
    p_helper.terminate()

    # verify expected output
    out = []
    while not r.empty():
        out.append(r.get())

    print(out)
    assert out >= ['f'] * 10

    # cleanup
    p_wander.join()
    p_helper.join()




