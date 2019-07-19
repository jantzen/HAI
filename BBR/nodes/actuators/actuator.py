""" Generic class for describing actuator nodes.
"""

from BBR.nodes.nodes import Node

class Actuator( Node ):

    def __init__(self, afferents):
        Node.__init__(self, afferents=afferents, efferents=None)

    def run(self):
        pass
