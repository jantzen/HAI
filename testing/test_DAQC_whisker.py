from BBR.nodes.sensors.DAQC_whisker import DAQC_Whisker
import multiprocessing as mp
import time

q = mp.Queue()
w = DAQC_Whisker([q], 0, 0)
p = mp.Process(target=w.run())
p.start()
time.sleep(10)
print(q.get())
