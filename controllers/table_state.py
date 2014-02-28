from event import DecisionMaker
from time import sleep
from math import sqrt
from sensors.pixels2coords import get_angle_from_pixels

import Queue

class TableState(DecisionMaker):


    def __init__(self, ev, lynx, controller):
        self.lynx = lynx
        self.controller = controller

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
                    self.controller.TurnInPlace(100, 'cw')
                    self.sleep(0.5)
                else:
                    self.speed=max(self.speed-50, 0) #self.speed/2
                    self.controller.DriveStraight(self.speed)
        self.controller.Stop()

    def faces_done(self, face):
        self.state = 'searching'
        self.lynx.setCam(-10)
        self.ev.unregister(event='faces_done', name='t_s')

    def table_pos(self, corners):
        if self.state == 'searching':
            self.state = 'fast'

        self.emit('obstacle_distance')

        length_right = sqrt((corners[0][0][0] - corners[3][0][0])**2 +
                            (corners[0][0][1] - corners[3][0][1])**2)
        length_left = sqrt((corners[1][0][0] - corners[2][0][0])**2 +
                           (corners[1][0][1] - corners[2][0][1])**2)
        print 'll = ', length_left, ', lr = ', length_right
        middle_x = (corners[0][0][0] + corners[2][0][0])/2
        angle = get_angle_from_pixels(middle_x, axis_size=4*1280/5)

        if self.state == 'fast':
            self.speed = min((self.speed + 50 ), 300)

        if length_left - length_right > 20:
            diff = 10
        elif length_right - length_left > 20:
            diff = -10
        else:
            diff = 0
            if abs(angle) < 5:
                self.controller.DriveStraight(self.speed)
            elif angle > 5:
                self.controller.TurnInPlace(2.5 * min(angle, 40), 'cw')
            else:
                self.controller.TurnInPlace(2.5 * max(angle, -40), 'cw')
            self.sleep(0.5)
            self.controller.Stop()
            return

        if angle > 0:
            self.controller.TurnInPlace(2.5 * min(angle, 40) + diff, 'cw')
        else:
            self.controller.TurnInPlace(2.5 * max(angle, -40) + diff, 'cw')
        self.sleep(0.5)
        self.controller.DriveStraight(100)
        self.sleep(1)
        self.controller.TurnInPlace(diff*1.5, 'ccw')
        self.sleep(0.5)
        self.controller.Stop()
        #self.sleep(0)
        print("angle")
        print(middle_x)
        print angle


    def obstacle(self, distance):
        print 'distance:', distance
        if distance < 30:
            self.stopping_frames += 1
            print "\nTable is close! %d\n" % self.stopping_frames
            self.speed = 0
            if self.stopping_frames > 3:
                self.state = 'park'

                print 'parking'
                self.controller.Stop()
                self.emit('cup_start')
                self.ev.unregister(event='frame', name='td')
                self.ev.register(event='frame', name='cd')

        elif distance <= 100:
            self.state = 'park'
            self.stopping_frames = 0
            print 'slowing down'
            self.speed = 50
        self.controller.DriveStraight(self.speed)
