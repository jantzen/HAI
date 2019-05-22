import piplates.Motorplate as motor
import time

isActivated = False

while (flag):
    time.sleep(0.1)
    stat = MOTOR.getSENSORS(0)
    if (stat & 0x2):
        isActivated = True


if isActivated == True:
    print ("bump switch activated!")
