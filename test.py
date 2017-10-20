import time
from bot import Bot
    
#init
bot = Bot()

#test movements
bot.move(50)
time.sleep(1)
bot.stopAll()
