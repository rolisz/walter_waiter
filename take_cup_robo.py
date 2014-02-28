#! /usr/bin/python

from controllers.cup_state import CupState
from controllers.face_state import FaceState
from controllers.nxt_controller import NxtController
from controllers.table_state import TableState
from sensors.webcam import Webcam, CupDetector, FaceDetector, TableDetector
from motors import lynx_motion
from sensors.ultrasonic import Ultrasonic
from event import EventLoop
from motors.pyrobot import Create


if __name__ == "__main__":
    e = EventLoop()
    lynx = lynx_motion.Arm()
    c_s = CupState(e, lynx, cam_angle=-25)
    ud = Ultrasonic(e)
    irobot_controller = Create()
    irobot_controller.Control()
    f_s = FaceState(e, irobot_controller)
    t_s = TableState(e, lynx, irobot_controller)
    cd = CupDetector(e, cam_angle=-25)
    fd = FaceDetector(e)
    td = TableDetector(e)
    n_c = NxtController(e)

    e.register('webcam', Webcam(e, cam=1))
    e.register('ultrasonic', ud)
    e.register('td', td, 'frame')
    e.register('cd', cd)
    e.register('fd', fd)  # We can see!

    # Events for cup taking actions
    e.register('c_s', c_s, 'cup_start')
    e.register('c_s', c_s, 'cup_appeared')  # Arm may align to grasp
    e.register('c_s', c_s, 'cup_grasped')  # Arm may align to release
    e.register('n_c', n_c, 'arm_aligned')  # Arm aligned for grasping
    e.register('n_c', n_c, 'cup_over_tray')  # Arm aligned for releasing
    e.register('c_s', c_s, 'cup_released')  # Arm may move to initial position

    # Events for face tracking and killing actions
    e.register('f_s', f_s, 'cups_done')
    e.register('f_s', f_s, 'face_pos')
    e.register('f_s', f_s, 'face_gone')
    e.register('f_s', f_s, 'no_cups_on_tray')

    # Events for going to the table
    e.register('t_s', t_s, 'faces_done')
    e.register('t_s', t_s, 'table_pos')

    # Obstacle avoidance
    e.register('n_c', n_c, 'obstacle_distance')  # Request
    e.register('t_s', t_s, 'obstacle')

    e.run()
