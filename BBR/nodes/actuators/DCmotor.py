"""Contains the template classes for describing DC motor actuators.
"""
from BBR.nodes.actuators.actuator import *
import queue

class Motor( Actuator ):
    """Generic class describing DC motors.
    """

    def __init__(self, afferents, efferents=None):
        Actuator.__init__(self, afferents, efferents)

    def config(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def forward(self):
        pass

    def reverse(self):
        pass

    def run(self):
        while self._run:
            try:
                cmd = None
                for aff in self._afferents:
                    if not aff.empty():
                        cmd = aff.get()
                        break
                if cmd == 'a':
                    self.start()
                elif cmd == 's':
                    self.stop()
                elif cmd == 'f':
                    self.forward()
                elif cmd == 'r':
                    self.reverse()
                elif cmd == 'q':
                    self.quit()
                    break
            except queue.Empty:
                continue
            except:
                self._run = False
                self.stop()
                self.cleanup()

    def quit(self):
        print("Motor node quitting.")
        self.stop()
        self._run = False

#    def terminate(self, signum, frame):
#        print("terminating motor node process with signum={}".format(signum))
#        self._run = False
#        seld.stop()
#        self.cleanup()
#        sys.exit(0)


class MotorCluster( Actuator ):
    """Coordinated collections of motor objects.
    """
    def __init__(self, afferents, efferents=None):
        """ afferents - a list of list of afferents, one list for each motor 
        belonging to the cluseter
        """
        Actuator.__init__(self, afferents, efferents)


#class MotorSystem( Actuator ):
#    """Coordinated collections of motor objects.
#    """
#    def __init__(self, afferents, cluster_list):
#        """ afferents
#            motor_list - list of motor ID numbers belonging to the cluster
#        """
#        Actuator.__init__(self, afferents)
#        self._cluster_list = cluster_list
#
#    def left(self):
#        pass
#
#    def right(self):
#        pass
#
#    def cleanup(self):
#        pass
