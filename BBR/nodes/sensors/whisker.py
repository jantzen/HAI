from BBR.nodes.sensors.sensor import Sensor

class Whisker( Sensor ):
    """Generic class describing Whisker bump sensors"""


    def __init__(self, afferents, isActived = False, signal):
        self._afferents = [BumpNode,]
        self._isActivated = False
        #defult signal strength of board
        self._voltageSignal = signal
        

    def read(self):
        #while True:
            while(self._isActivated == False):
                time.sleep(0.1)
                
                #if signal strength changes then interrupt current process and move to interrupt handler
                if(signal > signal):
                    self._isActivated = True
            
            if(self._isActivated = True):
                #send off info to BumpNode
                
    

    def run():
       self.read()
       self.emergency_stop()
          

    def emergency_stop(self):
        
        try:
            self.run()

        except (KeyboardInterrupt, SystemExit):
            cleanup_stop_thread()
            sys.exit()
