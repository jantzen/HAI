# /usr/bin/python3

import multiprocessing as mp
import datetime
import time
import sys


class test():
    def __init__(self, queue):
        self._queue = queue

    def func(self):
        print("launching the loop")
        try:
            while True:
                self._queue.put(1)
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("  exiting loop")
        except Exception:
            print("terminating")
        sys.exit(0)


def main():
    q = mp.Queue()
    t = test(q)
    p = mp.Process(target=t.func)
    try:
        p.start()
        time.sleep(1.5)
        p.terminate()
        p.join()
    except:
        print("ended in exception")
    print(q.qsize())
    print(q.get())


if __name__ == '__main__':
    main()

