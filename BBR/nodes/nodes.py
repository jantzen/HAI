""" Description of generic node class.
"""

class Node( ):
    
    def __init__(self, afferents=None, efferents=None):
        self._afferents = afferents
        self._efferents = efferents

    def run(self):
        pass
