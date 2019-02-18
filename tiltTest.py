from bot import Bot
import Adafruit_LSM303
import time

lsm303 = Adafruit_LSM303.LSM303()
bot = Bot()

while True:
    accel,mag = lsm303.read()
    accel_x, accel_y, accel_z = accel

    #if(accel_x > ?):
        #bot.stopAll()
    
    if (accel_x < -650):
        bot.moveBack()
        
    
    if (accel_y < -550):
        bot.backTurn(left)
        
   
    if (accel_y > 475):
        bot.backTurn(right)
        
    


    time.sleep(1.0)
        
