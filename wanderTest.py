from bot import Bot
from random import choice
import time

bot = Bot()

while True:
    random_function_selector = [bot.move, bot.moveBack(50), bot.backTurn(right),bot.backTurn(left), bot.movingTurn(right), bot.movingTurn(left), bot.turn(right), bot.turn(left)]

    choice(random_function_selector)()

    time.sleep(1.0)
