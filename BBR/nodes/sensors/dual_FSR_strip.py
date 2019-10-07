""" Class for using a pair of FSR strip sensors to detect bumps.
"""

from BBR.nodes.sensors.sensor import Sensor
import piplates.DAQCplate as DAQC
import time


class Dual_FSR_strips( Sensor ):
    
    def __init__(self, 
            efferents, 
            board_address=2,
            fore_address=0,
            aft_address=1,
            fore_threshold=3.4, 
            aft_threshold=3.2, 
            delay=0.05):
        Sensor.__init__(self, afferents=None, efferents=efferents)
        self._board_address = board_address
        self._fore_address = fore_address
        self._aft_address = aft_address
        self._fore_threshold = fore_threshold
        self._aft_threshold = aft_threshold
        self._delay = delay


    def read(self):
        fore = DAQC.getADC(self._board_address, self._fore_address)
        aft = DAQC.getADC(self._board_address, self._aft_address)
        out = None
        if  fore > self._fore_threshold:
            out = 'F'
        elif aft > self._aft_threshold:
            out = 'R'
        return out


    def fire(self, msg):
        for eff in self._efferents:
            eff.put(msg)
            time.sleep(self._delay)


    def run(self):
        while True:
            msg = self.read()
            if not msg is None:
                self.fire(msg)
            time.sleep(self._delay)
        sys.exit(0)
