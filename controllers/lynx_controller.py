from get_angles import get_angles
from time import sleep
from motors import lynx_motion
import event


class LynxController(event.DecisionMaker):

    def __init__(self, ev, cam_angle=-30):
        self.cam_angle = cam_angle
        super(LynxController, self).__init__(ev)

    def run(self):

        self.init_angles = (77, 20, 62)

        # Initially move to initial position
        self.l = lynx_motion.Arm()
        self.l.setAngles(*self.init_angles)
        self.l.setCam(self.cam_angle)
        try:
            while True:
                event, coords = self.queue.get(True, 20000)
                print(event)
                if event == 'cup_appeared':
                    angles = get_angles(coords[0]-10, -coords[1]+50)
                    self.l.setAngles(*angles)

                    sleep(2)
                    # Emit arm_aligned
                    print 'Arm: arm_aligned'
                    self.emit('arm_aligned', coords)

                if event == 'cup_grasped':
                    a, b, c = get_angles(50, -200)
                    self.l.setAngles(a, b, c, time=3)
                    sleep(3)
                    # Emit lego cup_over_tray
                    self.emit('cup_over_tray', (50, -200))
                    print 'Cup over tray'

                if event == 'cup_released':
                    self.l.setCam(30)

        except KeyboardInterrupt:
            pass
