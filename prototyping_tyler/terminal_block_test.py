import piplates.MOTORplate as MOTOR
import time

flag = 1  
while(flag):
    time.sleep(0.1)
    stat = MOTOR.getSENSORS(1)
    if (stat & 0x40):
        flag = 0
        print "bump switch activated!"
    else:
        print "waiting for activation"
