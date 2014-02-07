from lynx_controller import LynxController
from cup import CupRecognizer
from event import EventLoop

if __name__ == "__main__":
    e = EventLoop()

    l_c = LynxController(e, cam_angle=-30)
    e.register(l_c, 'cup_appeared')
    e.register(CupRecognizer(e, cam=1, cam_angle=-30))
    e.run()
