# /usr/bin/python

import multiprocessing as mp
import Queue
import time
import sys

class tester( object ):
    def __init__(self, q):
        self._q = q

    def run(self):
        while True:
            try:
                tmp = self._q.get()
                if tmp == 'q':
                    break
                else:
                    print(tmp)
            except Queue.Empty:
                continue
            except:
                break

        sys.exit(0)

if __name__ == '__main__':
    q = mp.Queue(maxsize=1)
    t = tester(q)
    p = mp.Process(target=t.run)
    p.start()
    test = range(20)
    for n in test:
        q.put(n)
        time.sleep(0.01)
    q.put('q')
    time.sleep(0.01)
    p.join()
