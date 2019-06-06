from BBR.nodes.internodes.internodes import Internode

class Bump ( Internode ):
    """Class describing bump module"""
    def __init__(self,afferents,efferents):
        Internode.__init__(self,afferents=afferents, efferents=efferents)
        LeftMotors = MotorCluster.__init__(self, afferents, motor_list) 
        RightMotors = Motorcluster.__init__(self, afferents, motor_list)
        LeftBump = Sensor.__init__(self, efferents)
        RightBump = Sensor.__init__(self, efferents)
        BackBump = Sensor.__init__(self, efferents)
        FrontBump = Sensor.__init__(self,efferents)
        
    def run(self):
        while True:
            try:
                leftComm = None
                for eff in LeftBump._efferents:
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

            sys.exit(0)
            pass
