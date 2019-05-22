import piplates.MOTORplate as motor
import time

isActivated = False

while (isActivated == False):
    time.sleep(0.1)
    stat = MOTOR.getSENSORS(1)
    if (stat & 7x1):
        isActivated = True


while (isActivated == True):
    print ("bump switch activated!")
    isActivated = False
