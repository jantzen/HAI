""" Generic class for describing sensor nodes.
"""

from BBR.nodes.nodes import Node

class Sensor( Node ):

    def __init__(self, efferents, afferents=None):
        Node.__init__(self, afferents=afferents, efferents=efferents)


    def read(self):
        pass


    def fire(self):
        pass

