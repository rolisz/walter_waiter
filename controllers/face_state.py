from event import DecisionMaker
from sensors.pixels2coords import get_angle_from_pixels
from time import sleep


class FaceState(DecisionMaker):

    def __init__(self, ev, controller):
        self.controller = controller
        self.controller.Control()
        self.rotated = False
        self.movements = []
        self.ev = ev
        self.speed = 0
        super(FaceState, self).__init__(ev)

    def cups_done(self, _):
        self.controller.TurnInPlace(100, 'cw')  # maybe turn random amount
        self.sleep(2)
        self.controller.Stop()

    def face_pos(self, value):
        print('face')
        angle = -get_angle_from_pixels(value[0] + value[2]/2.0)
        print(angle)
        self.speed = min(self.speed + 10, 150)
        if abs(angle) < 5:
            self.controller.DriveStraight(self.speed)
        elif angle > 5:  # I have no ideea what I'm doing
            self.controller.Drive(self.speed, 25 - angle)
        else:
            self.controller.Drive(self.speed, -25 - angle)

    def face_gone(self, _):
        self.speed = max(self.speed - 20, 0)
        self.controller.DriveStraight(self.speed)
        if self.speed == 0:
            self.sleep(5)
            self.emit('cups_done')

    def no_face(self, face):
        self.controller.TurnInPlace(100, 'cw')
        self.sleep(1)
        self.controller.Stop()

    def no_cups_on_tray(self, _):
        self.ev.unregister(event='frame', name='fd')
        self.ev.register(event='frame', name='td')
        self.emit('people_done')

