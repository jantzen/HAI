from BBR.nodes.node import Node

class Internode( Node ):

    def __init__(self, afferents, efferents):
        Node.__init__(self, afferents=afferents,efferents=efferents)

    def run(self):
        pass
