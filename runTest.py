from bot import Bot
import Adafruit_LSM303
import time

lsm303 = Adafruit_LSM303.LSM303()
bot = Bot()

while True:
    accel,mag = lsm303.read()
    accel_x, accel_y, accel_z = accel
    print(accel_x,accel_y,accel_z)

    if (accel_x < -650):
        #bot.moveBack(50)
        print("Moving backwards")
    else:
        #bot.move(50)
        print("Moving forwards")
    if (accel_y < -550):
        #bot.backTurn(left)
        print("Moving left tires backwards")
    else:
        #bot.move(50)
        print("Moving forwards")
    if accel_y > 475:
        #bot.backTurn(right)
        print("Moving right ties backwards")
    else:
        #bot.move(50)
        print("Moving forwards")


    time.sleep(1.0)
        
