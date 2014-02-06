from event import EventConsumer
from pyrobot import Create


class RoboController(EventConsumer):

    def __init__(self):
        self.controller = Create()
        self.controller.Control()
        super(RoboController, self).__init__()

    def run(self):
        speed = 0
        while True:
            event, value = self.queue.get(True, 20000)
            print(event)
            if event == 'face_pos':
                speed = min(speed + 10, 150)
                self.controller.DriveStraight(speed)
            if event == 'face_gone':
                speed = max(speed - 20, 0)
                self.controller.DriveStraight(speed)

