import multiprocessing as mp
import time
import queue

def f(q):
    for i in range(20):
        q.put(i)
        time.sleep(0.05)


q = mp.Queue(maxsize=1)
p = mp.Process(target=f, args=(q,))

p.start()
for i in range(20):
    print(q.get())

