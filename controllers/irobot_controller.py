from event import EventConsumer
from motors.pyrobot import Create
from sensors.pixels2coords import get_angle_from_pixels
from time import sleep


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
                angle = -get_angle_from_pixels(value[0] + value[2]/2.0)
                print(angle)
                speed = min(speed + 10, 150)
                if abs(angle) < 5:
                    self.controller.DriveStraight(speed)
                elif angle > 5:
                    self.controller.Drive(speed, 25 - angle)
                else:
                    self.controller.Drive(speed, -25 - angle)
            if event == 'face_gone':
                speed = max(speed - 20, 0)
                self.controller.DriveStraight(speed)
                sleep(5)
                self.controller.TurnInPlace(100, -1)
                sleep(2)
                self.controller.DriveStraight(100)
                sleep(2)
                self.controller.Stop()
            if event == 'cup_released':
                self.controller.TurnInPlace(100, 'cw')
                sleep(2)
                self.controller.Stop()
