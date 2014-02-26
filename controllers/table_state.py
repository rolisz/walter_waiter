from event import DecisionMaker
from sensors.pixels2coords import get_angle_from_pixels
from time import sleep


class TableState(DecisionMaker):

    def __init__(self, ev, controller):
        self.controller = controller
        self.controller.Control()

        self.ev = ev
        self.speed = 0
        super(TableState, self).__init__(ev)

    def faces_served(self, face):
        print "we need to find the table"
