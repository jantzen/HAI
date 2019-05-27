import piplates.DAQCplate as DAQC
import time

class DAQC_Whisker(Whisker):
    
    def __init__(self):
        self._DAQC.intEnable(0)
        self._DAQC.getDINbit(0,2)
        
    def read(self):
        while(Whisker._isActivated == False):
            time.sleep(0.1)
            self._DAQC.getDINbit(0,2)
            if(self.DAQC.getDINbit(0,2) = 1):
                Whisker._isActivated = True

        print("bump detected")
                
            
            
            
