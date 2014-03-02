#! /usr/bin/python

from controllers.cup_state import CupState
from controllers.face_state import FaceState
from controllers.table_state import TableState
from sensors.webcam import Webcam, CupDetector, FaceDetector, TableDetector
from motors import lynx_motion
from motors.nxt_controller import NxtController
from sensors.ultrasonic import Ultrasonic
from event import EventLoop
from motors.pyrobot import Create


if __name__ == "__main__":
    e = EventLoop()

    lynx = lynx_motion.Arm()

    nxt = NxtController()
    irobot_controller = Create("/dev/ttyUSB1")
    irobot_controller.Control()
    ud = Ultrasonic(e)

    c_s = CupState(e, lynx, nxt, cam_angle=-25)
    f_s = FaceState(e, lynx, irobot_controller)
    t_s = TableState(e, lynx, nxt, irobot_controller)
    cd = CupDetector(e, cam_angle=-25)
    fd = FaceDetector(e)
    td = TableDetector(e)

    e.register('webcam', Webcam(e, cam=1))
    e.register('ultrasonic', ud)
    e.register('td', td, 'frame')
    # e.register('td', td)
    e.register('cd', cd)
    e.register('fd', fd)  # We can see!
    # e.register('fd', fd, 'frame')  # We can see!

    # Events for cup taking actions
    e.register('c_s', c_s, 'cup_start')
    e.register('c_s', c_s, 'cup_appeared')  # Arm may align to grasp

    # Events for face tracking and killing actions
    e.register('f_s', f_s, 'cups_done')
    e.register('f_s', f_s, 'face_pos')
    e.register('f_s', f_s, 'face_gone')
    e.register('f_s', f_s, 'no_cups_on_tray')

    # Events for going to the table
    e.register('t_s', t_s, 'faces_done')
    e.register('t_s', t_s, 'table_pos')

    # e.add_event('cups_done', None)
    e.add_event('faces_done', None)

    e.run()
