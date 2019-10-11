""" Description of generic node class.
"""

import signal
import sys

class Node( ):
    
    def __init__(self, afferents=None, efferents=None):
        self._afferents = afferents
        self._efferents = efferents
        self._run = True
        signal.signal(signal.SIGINT, self.terminate)
        signal.signal(signal.SIGTERM, self.terminate)


    def run(self):
        pass


    def terminate(self, signum, frame):
        print("terminating node process with signum={}".format(signum))
        self._run = False
        sys.exit(0)
