import piplates.Motorplate as motor
import time

flag = False

while (flag):
    time.sleep(0.1)
    stat = MOTOR.getSENSORS(0)
    if (stat & 0x2):
        flag = True


if flag == True:
    print ("bump switch activated!")
