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

        # searching - still looking for image
        # fast - going for the SIFT image
        # park - sensor hit and we have to stop
        self.state = ''

        super(TableState, self).__init__(ev)

    def run(self):
        while self.run_flag.is_set():
            try:
                event, value = self.queue.get(True, 1)
                getattr(self, event)(value)
            except Queue.Empty:
                print 'table state: ', self.state
                if self.state == 'searching':
                    self.irobot.TurnInPlace(100, 'cw')
                    self.sleep(1)
                    self.irobot.Stop()
                    self.sleep(1)
                elif self.state != '':
                    self.speed = max(self.speed - 50, 0)
                    self.irobot.DriveStraight(self.speed)
        self.irobot.Stop()

    def faces_done(self, face):
        print 'what'
        self.state = 'searching'
        self.lynx.setCam(0)
        self.sleep(1)
        self.ev.unregister(event='no_cups_on_tray', name='f_s')

    def logo_properties(self, corners):
        length_right = sqrt((corners[0][0][0] - corners[3][0][0])**2 +
                            (corners[0][0][1] - corners[3][0][1])**2)
        length_left = sqrt((corners[1][0][0] - corners[2][0][0])**2 +
                           (corners[1][0][1] - corners[2][0][1])**2)
        middle_x = (corners[0][0][0] + corners[2][0][0])/2
        return length_right, length_left, middle_x

    def table_pos(self, corners):
        if self.state == 'searching':
            self.state = 'fast'

        is_blocked = self.checkObstacle()

        if is_blocked:
            return

        if self.state == 'fast':
            self.speed = min((self.speed + 50 ), 300)

        length_left, length_right, middle_x = self.logo_properties(corners)
        angle = get_angle_from_pixels(middle_x, axis_size=4*1280/5)
        if angle > 0:
            angle = min(angle, 40)
        else:
            angle = max(angle, -40)

        if abs(angle) < 5:
            self.irobot.DriveStraight(self.speed)
        else:
            self.irobot.TurnInPlace(2.5 * angle, 'cw')
            self.sleep(1)
            self.irobot.Stop()
        print("angle")
        print(middle_x)
        print angle


    def checkObstacle(self):
        values = []
        for i in range(5):
            values.append(self.nxt.getObstacleDistance())
            sleep(0.02)
        distance = sum(values)/5.0
        print 'distance:', distance

        if distance < 30:
            self.state = ''
            print 'parking'
            self.speed = 0
            self.irobot.Stop()
            self.emit('cup_start')
            self.ev.unregister(event='frame', name='td')
            self.ev.register(event='frame', name='cd')
            self.sleep(0)
            return True
        elif distance <= 100:
            self.state = 'park'
            self.speed = max(self.speed - 30, 50)
