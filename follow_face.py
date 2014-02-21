#! /usr/bin/python

from controllers.irobot_controller import RoboController
from sensors.webcam import Webcam, FaceDetector
from event import EventLoop
import sys

if __name__ == "__main__":
    e = EventLoop()

    r_c = RoboController(e.run_flag)
    fd = FaceDetector(e)

    e.register('fd', fd, 'frame')  # We can see!

    e.register('r_c', r_c, 'no_cup')  # When no cup, spin my head right round
    e.register('r_c', r_c, 'face_gone')  # Face disappeared, wait for pickup
    e.register('r_c', r_c, 'no_face')  # No face detected, try rotating
    e.register('r_c', r_c, 'face_pos')  # Face detected
    e.register('webcam', Webcam(e, cam=1))

    e.run()
