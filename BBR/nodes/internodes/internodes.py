from BBR.nodes.nodes import Node

class Internode( Node ):

    def __init__(self, afferents, efferents):
        Node.__init__(self, afferents,efferents)


    def read(self):
        pass


    def fire(self):
        pass

    
    def cleanup(self):
        pass
