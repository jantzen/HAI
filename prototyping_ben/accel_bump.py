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

def detect_impact(sensor, delta=0.04, epsilon=0.005):
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
        ay = np.array(ay).reshape(1,-1)
        az = np.array(az).reshape(1,-1)

        # compute mean magnitude of acceleration in horizontal plane
        mean_h = np.mean(np.sqrt(ax**2 + ay**2))
        std_h = np.std(np.sqrt(ax**2 + ay**2))

        # compute mean magnitude of vertical acceleration
        mean_v = np.mean(np.sqrt(az**2))
        std_v = np.std(np.sqrt(az**2))

        t1 = time.time()
        ax = []
        ay = []
        az = []
        while time.time() < t1 + epsilon:
            xtmp, ytmp, ztmp = sensor.acceleration
            ax.append(xtmp)
            ay.append(ytmp)
            az.append(ztmp)
            time.sleep(0.00125)
        ax = np.array(ax).reshape(1,-1)
        ay = np.array(ay).reshape(1,-1)
        az = np.array(az).reshape(1,-1)

        if (np.max(np.sqrt(ax**2 + ay**2)) > mean_h + 5. * std_h or 
                np.max(np.sqrt(az**2)) > mean_v + 5. * std_v):
            print("Bump detected!")


def main():
    try:
        sensor = setup()
        detect_impact(sensor)
    except KeyboardInterrupt:
        print("User interrupt detected. Exiting program...")

if __name__ == '__main__':
    main()


