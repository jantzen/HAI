from BBR.nodes.sensors.DAQC_whisker import DAQC_Whisker
import multiprocessing as mp
import time
import queue

q = mp.Queue(maxsize=1)
w = DAQC_Whisker([q], 0, 0)
p = mp.Process(target=w.run)
try:
    print("Starting process...")
    p.start()
    time.sleep(5.)
    print("Terminating process...")
    p.terminate()
    p.join()
except:
    print("  ended in exception")

qsize = q.qsize()
print("Queue size: {}".format(qsize))
print("Contents: ")
for ii in range(qsize):
    try:
        print(q.get_nowait())
    except queue.Empty:
        print("no items in queue")
