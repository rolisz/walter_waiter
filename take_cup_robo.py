from controllers.lynx_controller import LynxController
from controllers.irobot_controller import RoboController
from controllers.nxt_controller import NxtController
from sensors.webcam import Webcam, CupDetector, FaceDetector
from event import EventLoop
import sys

if __name__ == "__main__":
    e = EventLoop()

    l_c = LynxController(e, cam_angle=-25)
    n_c = NxtController(e)
    r_c = RoboController()
    cd = CupDetector(e)
    fd = FaceDetector(e)
    e.register(l_c, 'cup_appeared')  # Arm may align to grasp
    e.register(l_c, 'cup_grasped')  # Arm may align to release
    e.register(n_c, 'arm_aligned')  # Arm aligned for grasping
    e.register(n_c, 'cup_over_tray')  # Arm aligned for releasing
    e.register(l_c, 'cup_released')  # Arm may move to initial position
    e.register(n_c, 'cup_released')  # Arm may move to initial position                                 

    
    e.register(cd, 'frame')
    # TODO: only use frames for face det after 
    e.register(fd, 'frame')  # We can see!
    
    e.register(r_c, 'no_cup')  # When no cup, spin my head right round
    e.register(r_c, 'face_gone')  # Face disappeared, wait for drink pickup
    e.register(r_c, 'no_face')  # No face detected, try rotating
    e.register(r_c, 'face_pos')  # Face detected
    e.register(Webcam(e, cam=1, cam_angle=-25))
    e.add_event('cup_released', True)
    try:
        e.run()
    except (KeyboardInterrupt, SystemExit):
        #cleanup
        sys.exit()
