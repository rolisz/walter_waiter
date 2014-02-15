from controllers.lynx_controller import LynxController
from controllers.irobot_controller import RoboController
from controllers.nxt_controller import NxtController
from sensors.webcam import Webcam
from event import EventLoop
import sys

if __name__ == "__main__":
    e = EventLoop()

    l_c = LynxController(e, cam_angle=-25)
    n_c = NxtController(e)
    r_c = RoboController()
    e.register(l_c, 'cup_appeared')
    e.register(l_c, 'cup_grasped')
    e.register(n_c, 'arm_aligned')
    e.register(n_c, 'cup_over_tray')
    e.register(r_c, 'face_gone')
    e.register(r_c, 'face_pos')
    e.register(r_c, 'cup_released')
    e.register(Webcam(e, cam=1, cam_angle=-25))
    e.add_event('cup_released', True)
    try:
        e.run()
    except (KeyboardInterrupt, SystemExit):
        #cleanup
        sys.exit()
