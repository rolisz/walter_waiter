from event import EventConsumer
from pyrobot import Create


class RoboController(EventConsumer):

    def __init__(self):
        self.controller = Create()
        self.controller.Control()
        super(RoboController, self).__init__()

    def run(self):
        while True:
            event, value = self.queue.get(True, 20000)
            print(event)
            if event == 'face_pos':
                self.controller.smoothDriveStraight(100, 0.1)
            if event == 'face_gone':
                self.controller.Stop()

