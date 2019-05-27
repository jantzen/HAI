""" Generic class for describing actuator nodes.
"""

from BBR.nodes.nodes import Node

class Sensor( Node ):

    def __init__(self, efferents):
        self._afferents = afferents
        self._efferents = efferents

    def run(self):
        pass
