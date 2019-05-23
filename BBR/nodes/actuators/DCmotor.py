"""Contains the template classes for describing DC motor actuators.
"""

class Motor( object ):
    """Generic class describing DC motors.
    """

    def __init__(self):
        pass

    def config(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def left(self):
        pass

    def right(self):
        pass

    def forward(self):
        pass

    def reverse(self):
        pass

class MotorCluster( object ):
    """Coordinated collections of motor objects.
    """
    pass
