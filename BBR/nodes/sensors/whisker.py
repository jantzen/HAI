from BBR.nodes.sensors.sensor import Sensor
import sys
import time

class Whisker( Sensor ):
    """Generic class describing Whisker bump sensors"""


    def __init__(self, efferents, delay=0.1):
        Sensor.__init__(self, efferents)
        self._delay = delay
        

    def read(self):
        """Returns 1 if whisker has been touched since last poll, and 0
        otherwise.
        """
        pass
               

    def fire(self):
        # send message out efferents
        print("bump detected") #DEBUGGING
        for eff in self._efferents:
            eff.put(1)


    def cleanup(self):
        pass


    def run(self):
        while True:
            try:
                touch = self.read()
                if touch:
                    self.fire()
                time.sleep(self._delay)

            except:
                self.cleanup()
                sys.exit()

