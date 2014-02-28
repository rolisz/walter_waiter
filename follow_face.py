#! /usr/bin/python

from controllers.cup_state import CupState
from controllers.face_state import FaceState
from controllers.nxt_controller import NxtController
from sensors.webcam import Webcam, CupDetector, FaceDetector
from event import EventLoop
from motors.pyrobot import Create
import sys

if __name__ == "__main__":
    e = EventLoop()
    irobot_controller = Create()
    irobot_controller.Control()
    c_s = CupState(e, cam_angle=-25)

    f_s = FaceState(e, irobot_controller)
    cd = CupDetector(e, cam_angle=-25)
    fd = FaceDetector(e)

    e.register('webcam', Webcam(e, cam=1))
    e.register('fd', fd, 'frame')  # We can see!

    # Events for face tracking and killing actions
    e.register('f_s', f_s, 'cups_done')
    e.register('f_s', f_s, 'face_pos')
    e.register('f_s', f_s, 'face_gone')
    e.register('f_s', f_s, 'no_face')

    e.add_event('cups_done', None)
    e.run()
