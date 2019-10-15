from BBR.nodes.internodes.internodes import Internode
import time
from numpy.random import normal


class Wander( Internode ):
    """An internode class for generating random 
    (but generally forward) wandering motion.
    """

    def __init__(self,
            efferents,
            afferents,
            mean=3., # mean of normal distribution of action delays
            std=1., # standard deviation of the distribution
            burst_size=10 # number of forward commands to send on fire
            ):

        if not len(efferents) >= 1:
            raise ValueError("There must be at least one efferent.")

        Internode.__init__(self, afferents, efferents)
        self._mean = mean
        self._std = std
        self._burst_size = burst_size


    def fire(self):
        print("Wander node firing.")
        for ii in range(self._burst_size):
            for eff in self._efferents:
                if not eff.full():
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
                fire = True
                start = time.time()
                delay = max(normal(self._mean, self._std), 0.1)
                # wait for a random amount of time
                while time.time() < start + delay:
                        # check for a quit command
                        for aff in self._afferents:
                            if not aff.empty():
                                cmd = aff.get()
                                if cmd == 'q':
                                    self.quit()
                                    fire = False
                if fire:
                    # stimulate movement
                    self.fire()
            except KeyboardInterrupt:
                print("wander node received keyboard interrupt")
                self.quit()
            except:
                self.quit()


