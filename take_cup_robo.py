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
    n_c = NxtController(e)
    f_s = FaceState(e, irobot_controller)
    cd = CupDetector(e, cam_angle=-25)
    fd = FaceDetector(e)

    e.register('webcam', Webcam(e, cam=1))
    e.register('cd', cd, 'frame')
    e.register('fd', fd)  # We can see!

    # Events for cup taking actions
    e.register('c_s', c_s, 'cup_appeared')  # Arm may align to grasp
    e.register('c_s', c_s, 'cup_grasped')  # Arm may align to release
    e.register('n_c', n_c, 'arm_aligned')  # Arm aligned for grasping
    e.register('n_c', n_c, 'cup_over_tray')  # Arm aligned for releasing
    e.register('c_s', c_s, 'cup_released')  # Arm may move to initial position

    # Events for face tracking and killing actions
    e.register('f_s', f_s, 'cups_done')
    e.register('f_s', f_s, 'face_pos')
    e.register('f_s', f_s, 'face_gone')


    e.run()
