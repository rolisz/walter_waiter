from get_angles import get_angles
from time import sleep
from motors import lynx_motion
import event


class LynxController(event.DecisionMaker):

    def __init__(self, ev, cam_angle=-30):
        self.cam_angle = cam_angle
        self.ev = ev
        self.cups_got = 0
        self.cup = False
        self.init_angles = (77, 20, 62)
        super(LynxController, self).__init__(ev)

    def run(self):

        # Initially move to initial position
        self.l = lynx_motion.Arm()
        self.l.setAngles(*self.init_angles)
        self.l.setCam(self.cam_angle)
        super(LynxController, self).run()

    def cup_appeared(self, coords):
        if self.cup:
            return
        if not self.cup:
            self.cup = True
        angles = get_angles(coords[0]-10, -coords[1]+50)
        self.ev.unregister(event='frame', name='cd')
        print(angles)
        self.ev.unregister(event='cup_appeared', name='l_c')
        self.sleep(1.5)

        self.l.setAngles(*angles)
        # Emit arm_aligned
        print 'Arm: arm_aligned'
        self.emit('arm_aligned', coords)

    def cup_grasped(self, _):
        # Positions for cups, in the order to avoid collisions
        positions = [(0, -270),
                     (0, -130)
                     ]

        cup_pos = positions[self.cups_got]
        a, b, c = get_angles(*cup_pos)
        self.l.setAngles(a, b, c, time=3)
        print("angles")
        self.sleep(3)
        # Emit lego cup_over_tray
        self.emit('cup_over_tray', (50, -200))
        print 'Cup over tray'

    def cup_released(self, _):
        self.cups_got += 1
        self.l.setAngles(*self.init_angles)
        self.sleep(1)
        if self.cups_got < 1:
            # Look for more cups
            self.ev.register(event='frame', name='cd')
            self.ev.register(event='cup_appeared', name='l_c')
        else:
            # Look for people
            self.l.setCam(30)
            self.ev.register(event='frame', name='fd')
        self.cup = False
