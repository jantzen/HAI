from BBR.nodes.sensors.whisker import Whisker
import piplates.DAQCplate as DAQC
import time

class DAQC_Whisker( Whisker ):
    
    def __init__(self, efferents, brd_addr, DINbit, edge='r', delay=0.1):
        Whisker.__init__(self, efferents, delay)
        self._brd_addr = brd_addr
        self._DINbit = DINbit
        self._edge = edge
        DAQC.intEnable(brd_addr)
        DAQC.enableDINint(self._brd_addr, self._DINbit, self._edge) 
         

    def read(self):
        return DAQC.getDINbit(self._brd_addr, self._DINbit)
