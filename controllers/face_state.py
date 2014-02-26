from event import DecisionMaker
from Queue import Queue
from sensors.pixels2coords import get_angle_from_pixels
from time import sleep
from threading import Timer


class FaceState(DecisionMaker):

    def __init__(self, ev, controller):
        self.controller = controller
        self.controller.Control()
        self.ev = ev
        self.speed = 0

        self.status = 'done'

        super(FaceState, self).__init__(ev)

    def run(self):
        while self.run_flag.is_set():
            try:
                event, value = self.queue.get(True, 4)
                getattr(self, event)(value)
            except Queue.Empty:
                if self.state == 'finding':
                    self.rotate()

    def cups_done(self, _):
        print 'cups done, finding faces now'
        self.ev.unregister(event='frame', name='td')
        self.status = 'finding'

    def rotate(self):
        self.controller.TurnInPlace(20, 'cw')  # maybe turn random amount
        self.sleep(1)
        self.controller.Stop()

    def face_pos(self, value):
        if self.status in ['finding', 'tracking']:
            self.status = 'tracking'
            print('tracking face')
            angle = -get_angle_from_pixels(value[0] + value[2]/2.0)
            print(angle)
            self.speed = min(self.speed + 10, 150)
            if abs(angle) < 5:
                self.controller.DriveStraight(self.speed)
            elif angle > 5:  # I have no ideea what I'm doing
                self.controller.Drive(self.speed, 25 - angle)
            else:
                self.controller.Drive(self.speed, -25 - angle)
            self.sleep(0)
        else:
            print "we're done, somebody forgot to unregister fd"
            self.ev.unregister(event='frame', name='fd')
            self.ev.register(event='frame', name='td')
            return

    def face_gone(self, face):
        # Slow down
        self.speed = max(self.speed - 20, 0)
        self.controller.DriveStraight(self.speed)

        if self.speed == 0:
            print 'now youre gone: ' + self.status
            if self.status == 'done':
                print "we're done, somebody forgot to unregister fd"
                self.ev.unregister(event='frame', name='fd')
                self.ev.register(event='frame', name='td')
                return
            elif self.status == 'tracking':
                print 'lost track of face:', face
                if face[1] < 100:  # TODO: test
                    # We got to the face
                    self.sleep(5)

            # We lost the face, or we're done with
            self.status = 'finding'
            self.rotate()

    def no_cups_on_tray(self, _):
        self.ev.unregister(event='frame', name='fd')
        self.ev.register(event='frame', name='td')
        self.status = 'done'
        print 'faces served'
        self.emit('faces_served')
