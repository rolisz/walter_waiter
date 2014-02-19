from get_angles import get_angles
from time import sleep
from motors import lynx_motion
import event


class LynxController(event.DecisionMaker):

    def __init__(self, ev, cam_angle=-30):
        self.cam_angle = cam_angle
        self.ev = ev
        self.cups_got = 0
        self.init_angles = (77, 20, 62)
        super(LynxController, self).__init__(ev)

    def run(self):

        # Initially move to initial position
        self.l = lynx_motion.Arm()
        self.l.setAngles(*self.init_angles)
        self.l.setCam(self.cam_angle)
        super(LynxController, self).run()

    def cup_appeared(self, coords):
        angles = get_angles(coords[0]-10, -coords[1]+50)
        self.l.setAngles(*angles)

        sleep(1.5)
        # Emit arm_aligned
        print 'Arm: arm_aligned'
        self.emit('arm_aligned', coords)
        self.ev.unregister(event='frame', name='cd')

    def cup_grasped(self, _):

        if self.cups_got == 0:
            a, b, c = get_angles(0, -200-70)
        elif self.cups_got == 1:
            a, b, c = get_angles(0, -200+70)
        self.l.setAngles(a, b, c, time=3)
        print("angles")
        sleep(2)
        # Emit lego cup_over_tray
        self.emit('cup_over_tray', (50, -200))
        print 'Cup over tray'

    def cup_released(self, _):
        self.cups_got += 1
        self.l.setAngles(*self.init_angles)
        if self.cups_got < 2:
            # Look for more cups
            self.ev.register(event='frame', name='cd')
        else:
            # Look for people
            self.l.setCam(30)
            self.ev.register(event='frame', name='fd')
