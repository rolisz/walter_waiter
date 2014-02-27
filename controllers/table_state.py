from event import DecisionMaker
from sensors.pixels2coords import get_angle_from_pixels
from time import sleep
from sensors.pixels2coords import get_angle_from_pixels
import Queue

class TableState(DecisionMaker):


    def __init__(self, ev, controller):
        self.controller = controller

        self.ev = ev
        self.speed = 0
        super(TableState, self).__init__(ev)

    def run(self):
        while self.run_flag.is_set():
            try:
                event, value = self.queue.get(True, 1)
                getattr(self, event)(value)
            except Queue.Empty:
                self.speed=self.speed/2
                self.controller.DriveStraight(self.speed)
        self.controller.Stop()


    def faces_served(self, face):
        print "we need to find the table"

    def table_pos(self, corners):
        print(corners)
        middle_x = (corners[0][0][0] + corners[2][0][0])/2
        # length_x = abs(corners[0][0][0] - corners[2][0][0])
        # length_y = abs(corners[1][0][1] - corners[3][0][1])
        # middle_y = (corners[1] + corners[3])/2

        angle = get_angle_from_pixels(middle_x, axis_size=4*1280/5)
        self.speed = min(self.speed + 10, 100)
        if abs(angle) < 5:
            self.controller.DriveStraight(self.speed)
        elif angle > 5:  # I have no ideea what I'm doing
            self.controller.TurnInPlace(4*angle, 'cw')
            self.sleep(0.5)
            self.controller.Stop()
        else:
            self.controller.TurnInPlace(4*angle, 'cw')
            self.sleep(0.5)
            self.controller.Stop()

        print("angle")
        print(middle_x)
        print angle

