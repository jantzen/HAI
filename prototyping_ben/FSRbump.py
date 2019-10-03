# file: FSRbump.py

import piplates.DAQCplate as DAQC
import time

def detect(delay=0.05, thresh1=3.4, thresh2=3.2):
    i = 0
    while True:
        sensor1 = DAQC.getADC(2,0)
        sensor2 = DAQC.getADC(2,1)
        if i % 20 == 0:
            print(sensor1, sensor2)
        if  sensor1 > thresh1:
            print("Bump front")
        elif sensor2 > thresh2:
            print("Bump rear")
        time.sleep(delay)

if __name__ == '__main__':
    detect()
