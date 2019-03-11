from bot import Bot
import Adafruit_LSM303
import time

lsm303 = Adafruit_LSM303.LSM303()
bot = Bot()

while True:
    accel,mag = lsm303.read()
    accel_x, accel_y, accel_z = accel

    #if(accel_x > ?):
        #bot.stopAll()2
    
    if (accel_x < -650):
        print("rad")
        
    
    if (accel_y < -550):
        print("cool")
        
   
    if (accel_y > 475):
        print("right on")
        
    


    time.sleep(1.0)
        
