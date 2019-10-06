""" Generic class for describing actuator nodes.
"""

from BBR.nodes.nodes import Node

class Actuator( Node ):

    def __init__(self, afferents, efferents=None):
        Node.__init__(self, afferents=afferents, efferents=efferents)

    def run(self):
        pass
