# file: accel_bump.py

import board
import busio
import adafruit_mma8451
import time
import numpy as np

def setup():
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_mma8451.MMA8451(i2c)
    sensor.data_rate = adafruit_mma8451.DATARATE_800HZ
    return sensor

def detect_impact(sensor, 
        delta=0.05,
        thresh_h=3.,
        thresh_v=11.,
        ):
    while True:
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
            elif mx > 0. and my < 0.:
                print("Rear right bump detected.")
                print(mean_h)
                print(mx, my)
            elif mx < 0. and my > 0.:
                print("Front left bump detected.")
                print(mean_h)
                print(mx, my)
            elif mx < 0. and my < 0.:
                print("Front right bump detected.")
                print(mean_h)
                print(mx, my)
        if mean_v > thresh_v:
            print("Vertical bump detected.")
            print(mean_v)

def main():
    try:
        sensor = setup()
        detect_impact(sensor)
    except KeyboardInterrupt:
        print("User interrupt detected. Exiting program...")

if __name__ == '__main__':
    main()


