from BBR import *
import Adafruit_LSM303
import piplates.DAQCplate as DAQC
import multiprocessing as mp
import time
import queue

#def test_dcmotor_cluster():

#def test_dcmotor_run():

#def test_dcmotor_motorsystem():

#def test_dcmotor_motorplate_run():

#def test_whisker_run():

def test_right_DAQC_whisker_run():
    rightq = mp.Queue(maxsize = 1)
    rqsize = rightq.qsize()
    rightw = DAQC_Whisker([rightq], 0, 0)
    rightp = mp.Process(target = rightw.run)
    rightp.start()
    i = input("Please bump the right side, then press enter")
    if i:
        assert rqsize == 0
        rightp.terminate()
        rightp.join()
        
        


def test_right_DAQC_whisker_read():
    readright = mp.Queue(maxsize = 1)
    rrsize = readright.qsize()
    DAQC.intEnable(0)
    DAQC.enableDINint(0,0,'f')
    rightTmp = DAQC.getINTflags(0)
    if((2 ** 0) & rightTmp):
        readright.put(1)

    assert rrsize == 1    

def test_left_DAQC_whisker_run():
    leftq = mp.Queue(maxsize = 1)
    lqsize = leftq.qsize()
    leftw = DAQC_Whisker([leftq], 0, 3)
    leftp = mp.Process(target = leftw.run)
    leftp.start()
    i = input("Please bump the left side, then press enter")
    if i:
        assert lqsize == 1
        leftp.terminate()
        leftp.join()

def test_left_DAQC_whisker_read():
    readleft = mp.Queue(maxsize = 1)
    rlsize = readleft.qsize()
    DAQC.intEnable(0)
    DAQC.enableDINint(0, 3, 'f')
    leftTmp = DAQC.getINTflags(0)
    if((2 ** 3) & leftTmp):
       readleft.put(1)
    
    assert rlsize ==  1

       
def test_back_DAQC_whisker_run():
    bq = mp.Queue(maxsize = 1)
    bqsize = bq.qsize()
    bw = DAQC_Whisker([bq], 0, 1)
    bp = mp.Process(target = bw.run)
    bp.start()
    i = input("Please bump the back of robot, then press enter")
    if i:
        assert bqsize == 1
        bp.terminate()
        bp.join()

def test_back_DAQC_whisker_read():
    readback = mp.Queue(maxsize = 1)
    rbsize = readback.qsize()
    DAQC.intEnable(0)
    DAQC.enableDINint(0, 1, 'f')
    backTmp = DAQC.getINTflags(0)
    if((2 ** 1) & backTmp):
       readback.put(1)
    
    assert rbsize ==  1

def test_front_DAQC_whisker_run():
    fq = mp.Queue(maxsize = 1)
    fsize = fq.qsize()
    fw = DAQC_Whisker([fq], 0, 2)
    fp = mp.Process(target = fw.run)
    fp.start()
    i = input("Please bump the front of robot, then press enter")
    if i:
        assert fsize == 1
        fp.terminate()
        fp.join()
    
            
def test_front_DAQC_whisker_read():
    readfront = mp.Queue(maxsize = 1)
    rfsize = readfront.qsize()
    DAQC.intEnable(0)
    DAQC.enableDINint(0, 2, 'f')
    frontTmp = DAQC.getINTflags(0)
    if((2 ** 2) & frontTmp):
        readfront.put(1)
    
    assert rfsize ==  1

#def test_tilt_run():

def test_tiltLSM303_foward_read_run():
    qt = mp.Queue(maxsize = 1)
    tsize = qt.size()
    tf = Tilt_LSM303([qt], (0x28), (0x32 >> 1), (0x20))
    pt = mp.Process(target = tf.run)
    pt.start()
    i = input("Please tilt the robot forward, then press enter")
    if i:
        assert tsize == 1

def test_tiltLSM303_forward_read():
    tfr = Tilt_LSM303 (efferents = None, (0x28), (0x32 >> 1), (0x20))
    forward_detect = 0
    i = n():

def test_tiltLSM303_backwards_read():

#def test_tiltLSM303_right_run():

#def test_tiltLSM303_right_read():

#def test_tiltLSM303_left_run():

#def test_tiltLSM303_left_read():
