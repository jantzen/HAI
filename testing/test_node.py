
from BBR.nodes.nodes import Node
import multiprocessing as mp
import time
import signal
import pdb


class NodeMod( ):
    
    def __init__(self, afferents=None, efferents=None):
        self._afferents = afferents
        self._efferents = efferents
        self._run = True
        signal.signal(signal.SIGINT, self.terminate)
        signal.signal(signal.SIGTERM, self.terminate)


    def test_run(self, q):
        while self._run:
            print('writing to q')
            q.put(1)
            time.sleep(2)
        

    def terminate(self, signum, frame):
        print("terminating node process with signum={}".format(signum))
        self._run = False
        

def test_terminate():
    q = mp.Queue()
    tn = NodeMod()
    assert tn._run
    p = mp.Process(target=tn.test_run, args=(q,))
    p.start()
    time.sleep(5)
    p.terminate()
    p.join()
    assert q.qsize() >= 2
