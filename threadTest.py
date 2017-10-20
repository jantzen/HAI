import threading
import time
import random
import atexit
import signal

def command(message):
    #issue a new standing order from library of bot movements

class wander(threading.Thread):
    #def __init__(self):

    def run(self):
        self.stop_event = threading.Event()
        commands = ['forward', 'right', 'left']
        while (not self.stop_event.is_set()):
            command(random.choice(commands))
            self.stop_event.wait(random.uniform(0,3))

    def stop(self):
        self.stop_event.set()


#class reflexes(threading.Thread):
    #def __init__(self, threadId):
        #something

    #def run(self):
        #when sensors indicate problems, generate move commands to avoid
        #signal.pause()


#modes? wander mode, investigate mode
#some way to resolve conflicts between commands
#global function with a priority argument?
#maybe halt the entire wandering thread when avoiding an obstacle

#thread1 = wander()
#thread1.start()

#kill modules on exiting main program
def killModules():
    thread1.stop()
atexit.register(killModules)