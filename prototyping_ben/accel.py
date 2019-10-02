# file: accel.py

import board
import busio
import adafruit_mma8451
import time

def setup():
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_mma8451.MMA8451(i2c)
    sensor.data_rate = adafruit_mma8451.DATARATE_800HZ
    return sensor

def continuous_maximum(sensor):
    try:
        ii = 0
        ax_max = 0.
        ay_max = 0.
        az_max = 0.
        while(True):
            ax, ay, az = sensor.acceleration
            ax_max = max(ax, ax_max)
            ay_max = max(ay, ay_max)
            az_max = max(az, az_max)
            if ii % 800 == 0:
                print('ax_max = {0}, ay_max = {1}, az_max = {2}'.format(ax_max, ay_max, az_max))
                ax_max = 0.
                ay_max = 0.
                az_max = 0.
                ii = 0
            ii += 1
            time.sleep(0.00125)

    except KeyboardInterrupt:
        print("Exiting")

def main():
    sensor = setup()
    continuous_maximum(sensor)

if __name__ == '__main__':
    main()
