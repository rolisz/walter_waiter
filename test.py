#! /usr/bin/python

from sensors.webcam import Webcam, CupDetector, FaceDetector, TableDetector
from controllers.table_state import TableState

from controllers.nxt_controller import NxtController
from motors.pyrobot import Create
from event import EventLoop

import sys

if __name__ == "__main__":
    e = EventLoop()
    irobo = Create()
    irobo.Control()
    td = TableDetector(e)
    ts = TableState(e, irobo)
    n_c = NxtController(e)

    e.register('webcam', Webcam(e, cam=1))
    e.register('td', td, 'frame')
    e.register('ts', ts, 'table_pos')

    # Obstacle avoidance
    e.register('n_c', n_c, 'obstacle_distance')  # Request
    e.register('ts', ts, 'obstacle')

    e.run()
