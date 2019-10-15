""" Description of generic node class.
"""

import signal
import sys

class Node( ):
    
    def __init__(self, afferents=None, efferents=None):
        self._afferents = afferents
        self._efferents = efferents
        self._run = True
#        signal.signal(signal.SIGINT, self.terminate)
#        signal.signal(signal.SIGTERM, self.terminate)

    def run(self):
        while self._run:
            try:
                pass
            except:
                self._run = False

    def cleanup(self):
        pass

    def quit(self):
        self._run = False

#    def terminate(self, signum, frame):
#        print("terminating node process with signum={}".format(signum))
#        self._run = False
#        self.cleanup()
#        sys.exit(0)
