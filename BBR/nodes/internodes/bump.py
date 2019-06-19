from BBR.nodes.internodes.internodes import Internode
import time

class Bump ( Internode ):
    """Class describing bump module"""
    def __init__(self,afferents = [], efferents = [], delay = 0.1):
        Internode.__init__(self,afferents, efferents)
        
        
    def read(self):
        pass

    def fire(self):
         eff in LeftBump._efferents:
            if not eff.empty():
                leftComm = eff.get()
                break

        if leftComm == 1:
            for q in LeftMotors._afferents:
                q.put('f')
            for q in RightMotors._afferents:
                q.put('r')

        rightComm = None
        for eff in RightBump._efferents:
            if not eff.empy():
                rightComm = eff.get()
                break

        if rightComm == 1:
            for q in LeftMotors._afferents:
                q.put('r')
            for q in RightMotors._afferents:
                q.put('f')

        backComm = None
        for eff in BackBump._efferents:
            if not eff.empty():
                backComm = eff.get()
                break

        if backComm == 1:
            for q in LeftMotors._afferents:
                q.put('f')
            for q in RightMotors._afferents:
                q.put('r')

        frontComm = None
        for eff in FrontBump._efferents:
            if not eff.empty():
                frontComm = eff.get()

        if frontComm == 1:
            for q in LeftMotors._afferents:
                q.put('r')
            for q in RightMotors._afferents:
                q.put('r')

            
    def cleanup(self):
        pass
    
    def run(self):
        while True:
            try:
                bump = self.read()
                if bump:
                    self.fire()
                time.sleep(self._delay)

            except:
                self.cleanup()
                break

        sys.exit(0)

