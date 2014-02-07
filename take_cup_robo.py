from lynx_controller import LynxController
from cup import CupRecognizer
from nxt_controller import NxtController
from event import EventLoop

if __name__ == "__main__":
    e = EventLoop()

    l_c = LynxController(e, cam_angle=-30)
    n_c = NxtController(e)
    e.register(l_c, 'cup_appeared')
    e.register(l_c, 'cup_grasped')
    e.register(n_c, 'arm_aligned')
    e.register(n_c, 'cup_over_tray')
    e.register(CupRecognizer(e, cam=1, cam_angle=-30))
    e.run()
