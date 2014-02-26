from event import DecisionMaker
from sensors.pixels2coords import get_angle_from_pixels
from time import sleep
from sensors.pixels2coords import get_angle_from_pixels


class TableState(DecisionMaker):

    def __init__(self, ev, controller):
        self.controller = controller
        self.controller.Control()

        self.ev = ev
        self.speed = 0
        super(TableState, self).__init__(ev)

    def faces_served(self, face):
        print "we need to find the table"

    def table_pos(self, corners):
        print(corners)
        middle_x = (corners[0][0][0] + corners[2][0][0])/2
        # length_x = abs(corners[0][0][0] - corners[2][0][0])
        # length_y = abs(corners[1][0][1] - corners[3][0][1])
        # middle_y = (corners[1] + corners[3])/2

        angle = -get_angle_from_pixels(middle_x, axis_size=4*1280/5)
        if abs(angle) < 5:
            self.controller.DriveStraight(self.speed)
        elif angle > 5:  # I have no ideea what I'm doing
            self.controller.Drive(self.speed, 25 - angle)
        else:
            self.controller.Drive(self.speed, -25 - angle)

        print("angle")
        print(middle_x)
        print angle

