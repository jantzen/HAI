from BBR.nodes.node import Node

class Internode( Node ):

    def __init__(self, afferents, efferents):
        Node.__init__(self, afferents=afferents,efferents=efferents)

    def read(self):
        pass

    def fire(self):
        pass
    
    def run(self):
        pass
