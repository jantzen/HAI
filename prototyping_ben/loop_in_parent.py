import multiprocessing as mp
import time
import sys

class test():
    def __init__(self, queue):
        self._queue = queue

    def func(self):
        print("launching the child process loop")
        try:
            while True:
                self._queue.put(1)
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("keyboard interrupt received by child, exiting loop")
        except Exception:
            print("  terminating")
        sys.exit(0)


def main():
    q = mp.Queue()
    t = test(q)
    p = mp.Process(target=t.func)
    p.start()
    while True:
        try:
            time.sleep(3.)
        except KeyboardInterrupt:
            print("ending outer loop")
#            p.terminate()
            p.join()
            break
    qsize = q.qsize()
    print("Queue size: {}".format(qsize))
    for item in range(qsize):
        print(q.get())


if __name__ == '__main__':
    main()

