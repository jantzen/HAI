# /usr/bin/python3

import multiprocessing as mp
import datetime
import time

class tester( object ):
    def __init__(self):
        pass

    def foo(self, q):
        current = datetime.datetime.now()
        q.put(['hello', str(current)])

    def bar(self, q):
        time.sleep(0.5)
        current = datetime.datetime.now()
        q.put(['goodbye', str(current)])

class spawner( object ):
    def __init__(self):
        mp.set_start_method('spawn')
        q = mp.Queue()
        t = tester()
        p1 = mp.Process(target=t.foo, args=(q,))
        p2 = mp.Process(target=t.bar, args=(q,))
        p1.start()
        p2.start()
        print("First read from queue by parent process...")
        print(q.get())
        print("Second read from queue by parent process...")
        print(q.get())
        p1.join()
        p2.join()

if __name__ == '__main__':
    s = spawner()

