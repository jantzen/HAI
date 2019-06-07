from BBR.nodes.sensors.DAQC_whisker import DAQC_Whisker
from BBR.nodes.sensors.tiltLSM303 import Tilt_LSM303
import Adafruit_LSM303
import piplates.DAQCplate as DAQC
import multiprocessing as mp
import queue
import struct

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
        
        


#def test_right_DAQC_whisker_read():
    #readright = mp.Queue(maxsize = 1)
    #rrsize = readright.qsize()
    #DAQC.intEnable(0)
    #DAQC.enableDINint(0,0,'f')
    #rightTmp = DAQC.getINTflags(0)
    #if((2 ** 0) & rightTmp):
        #readright.put(1)

    #assert rrsize == 1    

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

#def test_left_DAQC_whisker_read():
    #readleft = mp.Queue(maxsize = 1)
    #rlsize = readleft.qsize()
    #DAQC.intEnable(0)
    #DAQC.enableDINint(0, 3, 'f')
    #leftTmp = DAQC.getINTflags(0)
    #if((2 ** 3) & leftTmp):
       #readleft.put(1)
    
    #assert rlsize ==  1

       
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

#def test_back_DAQC_whisker_read():
    #readback = mp.Queue(maxsize = 1)
    #rbsize = readback.qsize()
    #DAQC.intEnable(0)
    #DAQC.enableDINint(0, 1, 'f')
    #backTmp = DAQC.getINTflags(0)
    #if((2 ** 1) & backTmp):
       #readback.put(1)
    
    #assert rbsize ==  1

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
    
            
#def test_front_DAQC_whisker_read():
    #readfront = mp.Queue(maxsize = 1)
    #rfsize = readfront.qsize()
    #DAQC.intEnable(0)
    #DAQC.enableDINint(0, 2, 'f')
    #frontTmp = DAQC.getINTflags(0)
    #if((2 ** 2) & frontTmp):
        #readfront.put(1)
    
    #assert rfsize ==  1

#def test_tilt_run():

def test_tiltLSM303_forward_read_run():
    qt = mp.Queue(maxsize = 1)
    tsize = qt.qsize()
    tf = Tilt_LSM303([qt], (0x28), (0x32 >> 1), (0x20))
    ptf = mp.Process(target = tf.run)
    accel_raw = tf._accel.readList(tf._accel_address | 0x80, 6)
    accel = struct.unpack('<hhh', accel_raw)
    accel = (accel [0] >> 4, accel [1] >> 4, accel [2] >> 3)
    ptf.start() 
    i = input("Please tilt the robot forward to its tipping point, then press enter")
    if i:
        print(accel[0])
        assert tsize == 1
        
def test_tiltLSM303_backwards_read_run():
    qtb = mp.Queue(maxsize = 1)
    tbsize = qtb.qsize()
    tb = Tilt_LSM303([qtb], (0x28), (0x32 >> 1), (0x20))
    ptb = mp.Process(target = tb.run)
    accel_raw = tb._accel.readList(tb._accel_out | 0x80, 6)
    accel = struct.unpack('<hhh', accel_raw)
    accel = (accel [0] >> 4, accel [1] >> 4, accel [2] >> 3)
    ptb.start()
    i = input("Please tilt the robot backwards to its tipping point, then press enter")
    if i:
        print(accel[0])
        assert tsize == 1

def test_tiltLSM303_right_read_run():
    qtr = mp.Queue(maxsize = 1)
    trsize = qtr.qsize()
    tr = Tilt_LSM303([qtr], (0x28), (0x32 >> 1), (0x20))
    ptr = mp.Process(target = tr.run)
    accel_raw = tr._accel.readList(tr._accel_out | 0x80, 6)
    accel = struct.unpack('<hhh', accel_raw)
    accel = (accel [0] >> 4, accel [1] >> 4, accel [2] >> 3)
    ptr.start()
    i = input("Please tilt the robot to the left to  its tipping point, then press enter")
    if i:
        print(accel[1])
        assert tsize == 1

    

def test_tiltLSM303_left_read_run():
    qtl = mp.Queue(maxsize = 1)
    tlsize = qtl.qsize()
    tl = Tilt_LSM303([qtl], (0x28), (0x32 >> 1), (0x20))
    ptl = mp.Process(target = tl.run)
    accel_raw = tl._accel.readList(tl._accel_out | 0x80, 6)
    accel = struct.unpack('<hhh', accel_raw)
    accel = (accel [0] >> 4, accel [1] >> 4, accel [2] >> 3)
    ptl.start()
    i = input("Please tilt the robot to the right to its tipping point, then press enter")
    if i:
        print(accel[1])
        assert tsize == 1

