from BBR.nodes.sensors.sensor import Sensor
import sys
import time

class Tilt ( Sensor ):
    """Generic class describing tilt sensors"""

    def __init__(self,efferents, delay=0.1):
        Sensor.__init__(self, efferents)
        self._delay = delay

    def read(self):
        """Returns 1 if tilted too far, 0 otherwise"""
        pass

    def fire(self):
        print ("tilt detected")
        for eff in self._efferents:
            eff.put(1)


    def cleanup(self):
        pass


    def run(self):
        while True:
            try:
                tilted = self.read()
                if tilted:
                    self.fire()
                time.sleep(self._delay)

            except:
                self.cleanup()
                break

        sys.exit(0)
