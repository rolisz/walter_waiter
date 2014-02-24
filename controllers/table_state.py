from event import DecisionMaker
from sensors.pixels2coords import get_angle_from_pixels
from time import sleep


class TableState(DecisionMaker):

    def __init__(self, ev, controller):
        self.controller = controller
        self.controller.Control()
        self.slept = False
        self.ev = ev
        self.speed = 0
        super(TableState, self).__init__(ev)

    def face_pos(self, value):
        print('face')
        angle = -get_angle_from_pixels(value[0] + value[2]/2.0)
        print(angle)
        self.speed = min(self.speed + 10, 150)
        if abs(angle) < 5:
            self.controller.DriveStraight(self.speed)
        elif angle > 5:
            self.controller.Drive(self.speed, 25 - angle)
        else:
            self.controller.Drive(self.speed, -25 - angle)

    def face_gone(self, _):
        if not self.slept:
            self.speed = max(self.speed - 20, 0)
            self.controller.DriveStraight(self.speed)
            # if speed 0:
            # TODO: Play sound for human to take cup

        else:
            pass

    def no_cup(self, _):
        # We don't see any cups
        # A) find people to give them to
        # TODO: if tray sensor has cup:
        pass
        # Else:
        # emit locate cups

    def no_face(self, face):
        self.controller.TurnInPlace(100, 'ccw')
        self.sleep(1)
        self.controller.Stop()
        return
        # register for cups on tray
        x,y,w,h = face
        if x < 100:
            # The face has disappeared upwards
            # We need to wait for the people to pick up the cups
            self.ev.register(event='no_cups_on_tray', name='r_c')
        else:
            # We need to find faces
            self.ev.unregister(event='frame', name='fd')
            self.controller.TurnInPlace(100, 'cw')
            self.controller.Stop()
            self.ev.register(event='frame', name='fd')
        pass

    def cups_done(self, _):
        self.controller.TurnInPlace(100, 'cw')
        self.sleep(2)
        self.controller.Stop()

    def no_cups_on_tray(self, _):
        # TODO: Go back to table
        print 'Take me back to the table and restart the irobot if needed!'
        for i in range(30):
            if i % 5 == 0:
                print 30-i, 'seconds left.'
        pass
