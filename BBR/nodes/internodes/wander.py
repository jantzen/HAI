from BBR.nodes.internodes.internodes import Internode
import time
import numpy as np

class Wander( Internode ):
    """An internode class for generating random 
    (but generally forward) wandering motion.
    """

    def __init__(self,
            efferents,
            afferents,
            mean=2., # mean of normal distribution of action delays
            std=0.5, # standard deviation of the distribution
#            burst_size=10 # number of forward commands to send on fire
            ):

        if not len(efferents) >= 1:
            raise ValueError("There must be at least one efferent.")

        Internode.__init__(self, afferents, efferents)
        self._mean = mean
        self._std = std
#        self._burst_size = burst_size


    def fire(self):
        print("wander node firing.")
        index_array = np.arange(len(self._efferents))
        np.random.shuffle(index_array)
        for index in index_array:
            eff = self._efferents[index]
            if eff.full():
                print("wander node efferent {} is full".format(index))
            else:
                print("wander node sending msg to efferent {}".format(index))
                eff.put('f')
            time.sleep(0.05)


    def quit(self):
        print("wander node quitting")
        self._run = False
#        for eff in self._efferents:
#            eff.put('q', timeout=5)


    def run(self):
        while self._run:
            try:
                fire_status = True
                start = time.time()
                delay = max(np.random.normal(self._mean, self._std), 0.1)
                # wait for a random amount of time
                while time.time() < start + delay:
                        # check for a quit command
                        for aff in self._afferents:
                            if not aff.empty():
                                cmd = aff.get()
                                if cmd == 'q':
                                    self.quit()
                                    fire_status = False
                        time.sleep(0.05)
                if fire_status:
                    # stimulate movement
                    self.fire()
            except KeyboardInterrupt:
                print("wander node received keyboard interrupt")
                self.quit()
            except:
                print("wander node caught an exception")
                self.quit()


