import piplates.MOTORplate as MOTOR
import time

MOTOR.intEnable(1)
dummy = MOTOR.getINTflag0(1)

flag = 0

while(flag == 0):
    
    time.sleep(0.1)
    dummy1  = MOTOR.getINTflag0(1)
    formatdummy = "{0:b}".format(dummy1)
    if (dummy1 & 0x4):
        flag = 1

print("bump detected")        
