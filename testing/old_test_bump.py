from BBR.nodes.sensors.DAQC_whisker import DAQC_Whisker
from BBR.nodes.actuators.DCmotor_MOTORplate import RuntRoverSide
from BBR.nodes.internodes.bump import Bump
import multiprocessing as mp
import time
import queue

class RR_Bump (Bump):
    def __init__(self, afferents = [right_bump_queue, left_bump_queue, back_bump_queue, front_bump_queue], efferents = [left_motor_queue, right_motor_queue] ):
        Bump.__init__(self, afferents, efferents)
        left_bump_queue = mp.Queue(maxsize = 1)
        right_bump_queue = mp.Queue(maxsize = 1)
        back_bump_queue = mp.Queue(maxsize = 1)
        front_bump_queue = mp.Queue(maxsize = 1)
        left_motor_queue = mp.Queue(maxsize = 1)
        right_motor_queue = mp.Queue(maxsize = 1)
        right_whisker = DAQC_Whisker([right_bump_queue], 0, 0)
        left_whisker = DAQC_Whisker([left_bump_queue], 0, 3)
        back_whisker = DAQC_Whisker([back_bump_queue], 0, 1)
        front_whisker = DAQC_Whikser([front_bump_queue], 0, 2)
        p1 = mp.Process(target = right_whisker.run)
        p2 = mp.Process(target = left_whisker.run)
        p3 = mp.Process(target = back_whisker.run)
        p4 = mp.Process(target = front_whisker.run)
        RuntRoverLeft = RuntRoverSide([left_motor_queue],[1], 'cw', 'ccw', )
        RuntRoverRight = RuntRoverSide([right_motor_queue], [0], 'cw', 'ccw', )
        
    def read(self):
        if left_bump_queue = mp.Queue 
