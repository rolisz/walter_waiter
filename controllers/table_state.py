from event import DecisionMaker
from time import sleep
from math import sqrt
from sensors.pixels2coords import get_angle_from_pixels

import Queue

class TableState(DecisionMaker):


    def __init__(self, ev, controller):
        self.controller = controller

        self.ev = ev
        self.speed = 0
        self.stopping_frames = 0

        # fast - going for the SIFT image
        # park - sensor hit and we have to stop
        self.state = 'fast'

        super(TableState, self).__init__(ev)

    def run(self):
        while self.run_flag.is_set():
            try:
                event, value = self.queue.get(True, 1)
                getattr(self, event)(value)
            except Queue.Empty:
                self.speed=max(self.speed-50, 0) #self.speed/2
                self.controller.DriveStraight(self.speed)
        self.controller.Stop()


    def faces_served(self, face):
        print "we need to find the table"
        self.state = 'fast'
        # TODO: complete transition (connect self to  )

    def table_pos(self, corners):
        self.emit('obstacle_distance')

        length_right = sqrt((corners[0][0][0] - corners[3][0][0]) ** 2 + (corners[0][0][1] - corners[3][0][1])**2)
        length_left = sqrt((corners[1][0][0] - corners[2][0][0]) ** 2 + (corners[1][0][1] - corners[2][0][1])**2)
        print 'll = ', length_left, ', lr = ', length_right
        middle_x = (corners[0][0][0] + corners[2][0][0])/2
        # length_x = abs(corners[0][0][0] - corners[2][0][0])
        # length_y = abs(corners[1][0][1] - corners[3][0][1])
        # middle_y = (corners[1] + corners[3])/2
        self.sleep(0)
        angle = get_angle_from_pixels(middle_x, axis_size=4*1280/5)

        if self.state == 'fast':
            self.speed = min((self.speed + 50 ), 300)
        if abs(angle) < 5:
            self.controller.DriveStraight(self.speed)

        elif angle > 5:  # I have no ideea what I'm doing
            self.controller.TurnInPlace(2.5 * min(angle, 40), 'cw')
            self.sleep(0.5)
            self.controller.Stop()
        else:
            self.controller.TurnInPlace(2.5 * max(angle, -40), 'cw')
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
                self.ev.unregister(event='frame', name='ts')
                self.ev.register(event='frame', name='cd')

        elif distance <= 100:
            self.state = 'park'
            self.stopping_frames = 0
            print 'slowing down'
            self.speed = 50
        self.controller.DriveStraight(self.speed)
