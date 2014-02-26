#! /usr/bin/python

from sensors.webcam import Webcam, CupDetector, FaceDetector, TableDetector
from controllers.table_state import TableState
from motors.pyrobot import Create
from event import EventLoop

import sys

if __name__ == "__main__":
    e = EventLoop()
    irobo = Create()
    irobo.Control()
    td = TableDetector(e)
    ts = TableState(e, irobo)

    e.register('webcam', Webcam(e, cam=0))
    e.register('td', td, 'frame')
    e.register('ts', ts, 'table_pos')

    e.run()
