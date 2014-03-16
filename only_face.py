#! /usr/bin/python
from controllers.face_state import FaceState
from sensors.webcam import Webcam, FaceDetector
from event import EventLoop
from mock import Mock

class FakeIRobot(object):

    def Stop(self):
        print("Halt. Hammerzeit!")

    def DriveStraight(self, speed):
        print("Full speed ahead:", speed)

    def TurnInPlace(self, speed, direction):
        print("Turn around in direction", direction, " with speed ", speed)

    def Drive(self, speed, angle):
        print("I have no ideea: ", speed, angle)


if __name__ == "__main__":
    e = EventLoop()

    lynx = Mock()

    irobot_controller = FakeIRobot()

    f_s = FaceState(e, lynx, irobot_controller)
    fd = FaceDetector(e)

    e.register('webcam', Webcam(e, cam=1))
    e.register('fd', fd, 'frame')  # We can see!

    # Events for face tracking and killing actions
    e.register('f_s', f_s, 'cups_done')
    e.register('f_s', f_s, 'face_pos')
    e.register('f_s', f_s, 'face_gone')
    e.register('f_s', f_s, 'no_cups_on_tray')

    e.add_event('cups_done', None)

    e.run()
