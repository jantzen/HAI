from BBR.nodes.internodes.internodes import Internode
import sys
import time
from numpy.random import normal


class Wander( Internode ):
    """An internode class for generating random 
    (but generally forward) wandering motion.
    """

    def __init__(self,
            efferents,
            afferents=None,
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
        for ii in range(self._burst_size):
            for eff in self._efferents:
                if not eff.full():
                    eff.put('f')
            time.sleep(0.05)


    def run(self):
        while self._run:
            # wait for a random amount of time
            delay = max(normal(self._mean, self._std), 0.)
            time.sleep(delay)
            
            try:
                # stimulate movement
                self.fire()
            except:
                self.cleanup()
