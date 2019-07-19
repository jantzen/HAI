"""Contains the template classes for describing DC motor actuators.
"""
from BBR.nodes.actuators.actuator import *
import queue

class Motor( Actuator ):
    """Generic class describing DC motors.
    """

    def __init__(self, afferents):
        Actuator.__init__(self, afferents=afferents)

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
        while True:
            try:
                cmd = None
                for aff in self._afferents:
                    if not aff.empty():
                        cmd = aff.get()
                        break
                if cmd == 's':
                    self.stop()
                elif cmd == 'f':
                    self.forward()
                elif cmd == 'r':
                    self.reverse()
            except queue.Empty:
                continue
            except:
                self.cleanup()
                break

        sys.exit(0)
        pass


class MotorCluster( Actuator ):
    """Coordinated collections of motor objects.
    """
    def __init__(self, afferents, motor_list):
        """ afferents
            motor_list - list of motor ID numbers belonging to the cluster
        """
        Actuator.__init__(self, afferents)
        self._motor_list = motor_list


class MotorSystem( Actuator ):
    """Coordinated collections of motor objects.
    """
    def __init__(self, afferents, cluster_list):
        """ afferents
            motor_list - list of motor ID numbers belonging to the cluster
        """
        Actuator.__init__(self, afferents)
        self._cluster_list = cluster_list

    def left(self):
        pass

    def right(self):
        pass


