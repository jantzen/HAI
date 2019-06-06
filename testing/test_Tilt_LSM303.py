from BBR.nodes.sensors.tiltLSM303 import Tilt_LSM303
import multiprocessing as mp
import time
import queue

q = mp.Queue(maxsize = 1)
t = Tilt_LSM303 ([q],(0x28),(0x32 >> 1),( 0x20))
p = mp.Process(target=t.run)
try:
    print ("Starting process...")
    p.start
    time.sleep(5.)
    print("Terminating process...")
    p.terminate()
    p.join()
except:
    print(" ended in exeception")
qsize = q.qsize()
print("Queue size: {}".format(qsize))
print("Contents: ")
for x in range(qsize):
    try:
       print(q.get_nowait())
    except queue.Empty:
        print("no items in queue")
