""" Generic class for describing sensor nodes.
"""

from BBR.nodes.nodes import Node

class Sensor( Node ):

    def __init__(self, efferents):
        Node.__init__(self, afferents=None, efferents=efferents)


    def read(self):
        pass


    def fire(self):
        pass


    def run(self):
        pass
