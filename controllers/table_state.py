from event import DecisionMaker
from time import sleep
from math import sqrt
from sensors.pixels2coords import get_angle_from_pixels

import Queue

class TableState(DecisionMaker):
    def __init__(self, ev, lynx, nxt, irobot):
        self.lynx = lynx
        self.irobot = irobot
        self.nxt = nxt
        self.ev = ev
        self.speed = 0
        self.stopping_frames = 0

        # searching - still looking for image
        # fast - going for the SIFT image
        # park - sensor hit and we have to stop
        self.state = 'searching'

        super(TableState, self).__init__(ev)

    def run(self):
        while self.run_flag.is_set():
            try:
                event, value = self.queue.get(True, 1)
                getattr(self, event)(value)
            except Queue.Empty:
                if self.state == 'searching':
                    self.irobot.TurnInPlace(100, 'cw')
                    self.sleep(0.5)
                    self.irobot.Stop()
                    self.sleep(1)
                else:
                    self.speed = max(self.speed - 50, 0) #self.speed/2
                    self.irobot.DriveStraight(self.speed)
        self.irobot.Stop()

    def faces_done(self, face):
        self.state = 'searching'
        self.lynx.setCam(0)
        self.ev.unregister(event='no_cups_on_tray', name='f_s')

    def computeStuff(corners):
        length_right = sqrt((corners[0][0][0] - corners[3][0][0])**2 +
                            (corners[0][0][1] - corners[3][0][1])**2)
        length_left = sqrt((corners[1][0][0] - corners[2][0][0])**2 +
                           (corners[1][0][1] - corners[2][0][1])**2)
        middle_x = (corners[0][0][0] + corners[2][0][0])/2
        return length_right, length_left, middle_x

    def table_pos(self, corners):
        if self.state == 'searching':
            self.state = 'fast'

        obstacle = self.checkObstacle()

        length_left, length_right, middle_x = computeStuff(corners)
        angle = get_angle_from_pixels(middle_x, axis_size=4*1280/5)
        if angle > 0:
            angle = 2.5 * min(angle, 40)
        else:
            angle = 2.5 * max(angle, -40)

        if self.state == 'fast':
            self.speed = min((self.speed + 50 ), 300)

        if length_left - length_right > 20:
            diff = 30
        elif length_right - length_left > 20:
            diff = -30

        angle += diff

        if abs(angle) < 13:
            self.irobot.DriveStraight(self.speed)
        else:
            self.irobot.TurnInPlace(angle, 'cw')        

        self.sleep(0.5)
        self.irobot.DriveStraight(speed)
        self.sleep(1)
        self.irobot.TurnInPlace(diff, 'ccw')
        self.sleep(0.5)
        self.irobot.Stop()
        print("angle")
        print(middle_x)
        print angle


    def checkObstacle(self):
        distance = self.nxt.getObstacleDistance()
        print 'distance:', distance

        if distance < 30:
            self.stopping_frames += 1
            print "\nTable is close! %d\n" % self.stopping_frames
            self.speed = 0
            if self.stopping_frames > 3:
                self.state = 'park'

                print 'parking'
                self.irobot.Stop()
                self.emit('cup_start')
                self.ev.unregister(event='frame', name='td')
                self.ev.register(event='frame', name='cd')

        elif distance <= 60:
            self.state = 'park'
            self.stopping_frames = 0
            print 'slowing down'
            self.speed = 50