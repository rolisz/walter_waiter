from event import DecisionMaker
from time import sleep
import Queue
from sensors.pixels2coords import get_angle_from_pixels


class FaceState(DecisionMaker):

    def __init__(self, ev, irobot):
        self.irobot = irobot
        self.ev = ev
        self.speed = 0

        # done
        # finding
        # tracking
        self.status = 'done'

        super(FaceState, self).__init__(ev)

    def run(self):
        while self.run_flag.is_set():
            try:
                event, value = self.queue.get(True, 2)
                getattr(self, event)(value)
            except Queue.Empty:
                if self.status == 'finding':
                    self.rotate()
        self.irobot.Stop()


    def sleep(self, time):
        sleep(time)
        event = None
        value = None
        while True:
            try:
                event, value = self.queue.get(False)
            except Queue.Empty:
                try:
                    if event is not None:
                        self.queue.put((event, value))
                except AttributeError:
                    print("Unfound attribute %s" % event)
                break


    def cups_done(self, _):
        self.sleep(1)
        print 'cups done, finding faces now'
        self.ev.register(event='no_cups_on_tray', name='f_s')
        self.status = 'finding'
        self.irobot.DriveStraight(-100)
        self.irobot.DriveStraight(-100)
        sleep(3)
        self.irobot.Stop()
        self.rotate(10)
        self.sleep(0)

    def rotate(self, amount = 1.5):
        self.irobot.TurnInPlace(100, 'cw')  # maybe turn random amount
        print "bef sleep"
        sleep(amount)
        print "after sleep"
        self.irobot.Stop()
        print "after stop"
        self.sleep(0)

    def face_pos(self, value):
        if self.status in ['finding', 'tracking']:
            self.status = 'tracking'
            print('tracking face')
            angle = -get_angle_from_pixels(value[0] + value[2]/2.0)
            print(angle)
            self.speed = min(self.speed + 10, 150)
            if abs(angle) < 5:
                self.irobot.DriveStraight(self.speed)
            elif angle > 5:  # I have no ideea what I'm doing
                self.irobot.Drive(self.speed, 25 - angle)
            else:
                self.irobot.Drive(self.speed, -25 - angle)
            self.sleep(0)
        else:
            print "we're done, somebody forgot to unregister fd"

    def face_gone(self, face):
        # Slow down
        self.speed = max(self.speed - 20, 0)
        self.irobot.DriveStraight(self.speed)

        if self.speed == 0:
            print 'now youre gone: ' + self.status
            if self.status == 'done':
                print "we're done, somebody forgot to unregister fd"
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
        self.emit('faces_done')
