from event import EventConsumer
from motors.pyrobot import Create
from sensors.pixels2coords import get_angle_from_pixels
from time import sleep


class RoboController(EventConsumer):

    def __init__(self, ev):
        self.controller = Create()
        self.controller.Control()
        self.slept = False
        super(RoboController, self).__init__(ev)

    def face_pos(self, value):
        angle = -get_angle_from_pixels(value[0] + value[2]/2.0)
        print(angle)
        speed = min(speed + 10, 150)
        if abs(angle) < 5:
            self.controller.DriveStraight(speed)
        elif angle > 5:
            self.controller.Drive(speed, 25 - angle)
        else:
            self.controller.Drive(speed, -25 - angle)

    def face_gone(self, _):
        if not self.slept:
            speed = max(speed - 20, 0)
            self.controller.DriveStraight(speed)
            # TODO: Play sound for human to take cup
            if speed == 0:
                self.sleep(15)
                self.slept = True
        else:
            pass

    def no_cup(self, _):
        # We don't see any cups
        # A) find people to give them to
        # TODO: if tray sensor has cup:
        pass
        # Else:
        # emit locate cups

    def no_face(self, _):
        # Find a new face
        self.ev.unregister(event='frame', name='fd')
        self.controller.TurnInPlace(100, 'vw')        
        
        self.ev.register(event='frame', name='fd')
    
    def cups_done(self, _):
        self.controller.TurnInPlace(100, 'cw')
        sleep(2)
        self.controller.Stop()
