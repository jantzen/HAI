import piplates.MOTORplate as MOTOR
import time


MOTOR.intEnable(1) 

flag = 0  
while(flag == 0):
    time.sleep(0.1)
    stat = MOTOR.getSENSORS(1)
    "{0:b}".format(stat)
    #if (stat & 0x40):
        #flag = 1
        #print "bump switch activated!"
    #else:
        #print "waiting for activation"
    print(stat)
