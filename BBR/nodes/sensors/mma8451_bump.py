""" Class for using the Adafruit mma8451 as a bump sensor.
"""

# file: mma8451_bump.py

import board
import busio
import adafruit_mma8451
import time
import numpy as np

class mma8451_bump( Sensor ):

    def __init__(self,
            afferents,
            efferents,
            delta=0.05,
            thresh_h=3.,
            thresh_v=11.
            ):
            
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_mma8451.MMA8451(i2c)
        self.sensor.data_rate = adafruit_mma8451.DATARATE_800HZ
        self._delta=0.05,
        self._thresh_h=3.,
        self._thresh_v=11.


    def read(self ):
        t0 = time.time()
        ax = []
        ay = []
        az = []
        while time.time() < t0 + delta:
            xtmp, ytmp, ztmp = sensor.acceleration
            ax.append(xtmp)
            ay.append(ytmp)
            az.append(ztmp)
            time.sleep(0.00125)
        ax = np.array(ax).reshape(1,-1)
        mx = np.mean(ax)
        ay = np.array(ay).reshape(1,-1)
        my = np.mean(ay)
        az = np.array(az).reshape(1,-1)
        mz = np.mean(az)

        # compute mean magnitude of acceleration in horizontal plane
        mean_h = np.sqrt(mx**2 + my**2)

        # compute mean magnitude of vertical acceleration
        mean_v = np.sqrt(mz**2)

        if mean_h > thresh_h:
            if mx > 0. and my > 0.:
                print("Rear left bump detected.")
                print(mean_h)
                print(mx, my)
                out = 'R'
            elif mx > 0. and my < 0.:
                print("Rear right bump detected.")
                print(mean_h)
                print(mx, my)
                out = 'R'
            elif mx < 0. and my > 0.:
                print("Front left bump detected.")
                print(mean_h)
                print(mx, my)
                out = 'F'
            elif mx < 0. and my < 0.:
                print("Front right bump detected.")
                print(mean_h)
                print(mx, my)
                out = 'F'
        if mean_v > thresh_v:
            print("Vertical bump detected.")
            print(mean_v)
            out = 'V'
        return out


    def fire(self, msg):
        for eff in self._efferents:
            eff.put(msg)
            time.sleep(self._delay)


    def run(self):
        try:
            # check for quit command:
            for aff in self._afferents:
                if not aff.empty():
                    tmp = aff.get()
                    if tmp == 'q':
                        self.quit()
            msg = self.read()
            if not msg is None:
                self.fire(msg)
            time.sleep(self._delay)
        except KeyboardInterrupt:
            print("mma8451_bump node received keyboard interrupt")
            self.quit()
        except:
            self.quit()
