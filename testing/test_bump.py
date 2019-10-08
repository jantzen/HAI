# file: test_bump_internode.py
from BBR.nodes.internodes.bump import Bump
import multiprocessing as mp
import queue
import time


def test_msg_to_cmds():
    b = Bump([None, None], [None, None])
    cmd = b.msg_to_cmds('F')
    assert cmd == ['srrrrrsfs', 'srrrrrsfffffs']


def test_read():
    # make afferent queue
    aq = mp.Queue(maxsize=1)

    # make a pair of efferent queues (left, right)
    eq1 = mp.Queue(maxsize=1)
    eq2 = mp.Queue(maxsize=1)

    # create bump node
    b = Bump([aq],[eq1, eq2])

    # send a message in along afferent
    aq.put('F')
    time.sleep(0.1)

    # verify msg 
    msg = b.read()
    assert msg == 'F'


def test_fire():
    # make afferent queue
    aq = mp.Queue(maxsize=1)

    # make a pair of efferent queues (left, right)
    eq1 = mp.Queue(maxsize=1)
    eq2 = mp.Queue(maxsize=1)

    # create bump node
    b = Bump([aq],[eq1, eq2])

    # send a message in along afferent
    aq.put('F')
    time.sleep(0.1)

    # fire, and count the commands that come out on left and right
    cmds = b.msg_to_cmds('F')
    p = mp.Process(target=b.fire, args=(cmds,))
    p.start()
    time.sleep(0.1)
    left = 0
    right = 0
    while (not eq1.empty()) or (not eq2.empty()):
        if not eq1.empty():
            print("reading left")
            eq1.get()
            left += 1
        if not eq2.empty():
            print("reading right")
            eq2.get()
            right += 1
        time.sleep(0.1)
    p.join()
    print(left, right)
    assert left == 9
    assert right == 13


