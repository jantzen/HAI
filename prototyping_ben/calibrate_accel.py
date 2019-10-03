# file: accel.py

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


def gather_data(sensor, delta=5.):
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
    acc = np.array([ax,ay,az]).T
    ax = np.array(ax).reshape(1,-1)
    ay = np.array(ay).reshape(1,-1)
    az = np.array(az).reshape(1,-1)

    # compute mean magnitude of acceleration in horizontal plane
    mean_h = np.sqrt(np.mean(ax)**2 + np.mean(ay)**2)
#    std_h = np.std(np.sqrt(ax**2 + ay**2))

    # compute mean magnitude of vertical acceleration
    mean_v = np.sqrt(np.mean(az)**2)
#    std_v = np.std(np.sqrt(az**2))

#    return mean_h, std_h, mean_v, std_v
    return mean_h, mean_v

def calibrate(sensor):
    delta = 5

    try:
        # collect means and standard deviations of magnitudes of acceleration in the xy-plane

        # steady forward motion at 50
        print("Steady forward motion at level 50.")
        input("Press Enter when ready.")
        mean_h, mean_v = gather_data(sensor)
#        print("Recommended horizontal threshold: {}".format(mean_h + std_h))
#        print("Recommended vertical threshold: {}".format(mean_v + std_v))
        print("Recommended horizontal threshold: {}".format(mean_h))
        print("Recommended vertical threshold: {}".format(mean_v))

#        # steady reverse motion at 50
#        print("Steady reverse motion at level 50.")
#        input("Press Enter when ready.")
#        mean_h, std_h, mean_v, std_v = gather_data(sensor)
#        print("Recommended horizontal threshold: {}".format(mean_h + std_h))
#        print("Recommended vertical threshold: {}".format(mean_v + std_v))

        # rotate in place CW at 70
        print("Rotate in place CW at 70.")
        input("Press Enter when ready.")
#        mean_h, std_h, mean_v, std_v = gather_data(sensor)
        mean_h, mean_v = gather_data(sensor)
#        print("Recommended horizontal threshold: {}".format(mean_h + std_h))
#        print("Recommended vertical threshold: {}".format(mean_v + std_v))
        print("Recommended horizontal threshold: {}".format(mean_h))
        print("Recommended vertical threshold: {}".format(mean_v))

#        # rotate in place CCW at 70
#        print("Rotate in place CCW at 70.")
#        input("Press Enter when ready.")
#        mean_h, std_h, mean_v, std_v = gather_data(sensor)
#        print("Recommended horizontal threshold: {}".format(mean_h + std_h))
#        print("Recommended vertical threshold: {}".format(mean_v + std_v))
#
#        # forward collision at 30
#        print("Forward collision at 30.")
#        input("Press Enter when ready.")
#        mean_h, std_h, mean_v, std_v = gather_data(sensor)
#        print("Recommended horizontal threshold: {}".format(mean_h + std_h))
#        print("Recommended vertical threshold: {}".format(mean_v + std_v))
#
#        # reverse collision at 30
#        print("Reverse collision at 30.")
#        input("Press Enter when ready.")
#        mean_h, std_h, mean_v, std_v = gather_data(sensor)
#        print("Recommended horizontal threshold: {}".format(mean_h + std_h))
#        print("Recommended vertical threshold: {}".format(mean_v + std_v))
#
#        # right front oblique forward collision at 30
#        print("Right front oblique collision at 30.")
#        input("Press Enter when ready.")
#        mean_h, std_h, mean_v, std_v = gather_data(sensor)
#        print("Recommended horizontal threshold: {}".format(mean_h + std_h))
#        print("Recommended vertical threshold: {}".format(mean_v + std_v))
#
#        # left front oblique forward collision at 30
#        print("Left front oblique collision at 30.")
#        input("Press Enter when ready.")
#        mean_h, std_h, mean_v, std_v = gather_data(sensor)
#        print("Recommended horizontal threshold: {}".format(mean_h + std_h))
#        print("Recommended vertical threshold: {}".format(mean_v + std_v))
#
#        # right rear oblique forward collision at 30
#        print("Right rear oblique collision at 30.")
#        input("Press Enter when ready.")
#        mean_h, std_h, mean_v, std_v = gather_data(sensor)
#        print("Recommended horizontal threshold: {}".format(mean_h + std_h))
#        print("Recommended vertical threshold: {}".format(mean_v + std_v))
#
#        # left rear oblique forward collision at 30
#        print("Left rear oblique collision at 30.")
#        input("Press Enter when ready.")
#        mean_h, std_h, mean_v, std_v = gather_data(sensor)
#        print("Recommended horizontal threshold: {}".format(mean_h + std_h))
#        print("Recommended vertical threshold: {}".format(mean_v + std_v))

    except KeyboardInterrupt:
        print("Exiting")

def main():
    sensor = setup()
    calibrate(sensor)

if __name__ == '__main__':
    main()
