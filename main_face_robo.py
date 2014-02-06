from irobot_controller import RoboController
from face import FaceRecognizer
from event import EventLoop

if __name__ == "__main__":
    e = EventLoop()

    r_c = RoboController()
    e.register(r_c, 'face_gone')
    e.register(r_c, 'face_pos')
    e.register(FaceRecognizer(e, 1))

    e.run()
