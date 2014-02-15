from event import EventConsumer
from motors.pyrobot import Create
from sensors.pixels2coords import get_angle_from_pixels
from time import sleep


class RoboController(EventConsumer):

    def __init__(self):
        self.controller = Create()
        self.controller.Control()
        self.slept = False
        super(RoboController, self).__init__()

        event, value = self.queue.get(True, 20000)
        print(event)

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
        self.no_face(_)
        # Else:
        # emit locate cups

    def no_face(self, _):
        # Find a new face
        
    def cup_released(self, _):
        self.controller.TurnInPlace(100, 'cw')
        sleep(2)
        self.controller.Stop()
