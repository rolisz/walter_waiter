from get_angles import get_angles
from time import sleep
from motors import lynx_motion
import event


class CupState(event.DecisionMaker):

    def __init__(self, ev, cam_angle=-30):
        self.cam_angle = cam_angle
        self.ev = ev
        self.cups_got = 0
        self.cup = False
        self.init_angles = (77, 20, 62)
        super(CupState, self).__init__(ev)

    def run(self):
        # Move to initial position
        self.l = lynx_motion.Arm()
        self.l.setAngles(*self.init_angles)
        self.l.setCam(self.cam_angle)
        super(CupState, self).run()

    def cup_appeared(self, coords):
        if self.cup:
            return
        else:
            self.cup = True
        angles = get_angles(coords[0]-10, -coords[1]+50)
        self.l.setAngles(*angles)  # shouldn't there be a time here as well?
        self.sleep(2)
        # Emit arm_aligned
        print 'Arm: arm_aligned'
        self.emit('arm_aligned', coords)

    def cup_grasped(self, _):
        # Positions for cups, in the order to avoid collisions
        positions = [(0, -270),
                     (100, -200) # TODO: test
                     ]

        cup_pos = positions[self.cups_got]
        a, b, c = get_angles(*cup_pos)
        self.l.setAngles(*self.init_angles)
        self.sleep(1)
        self.l.setAngles(a, b, c, time=3)
        self.sleep(3)
        # Emit lego cup_over_tray
        self.emit('cup_over_tray', (50, -200))
        print 'Cup over tray'

    def cup_released(self, _):
        self.cups_got += 1
        self.l.setAngles(*self.init_angles)
        self.sleep(1)
        if self.cups_got == 2:
            self.ev.unregister(event='frame', name='cd')
            self.ev.register(event='frame', name='fd')
            print 'emitting cups_done' # TODO: Haven't checked if this runs!!!
            self.emit('cups_done')
            self.l.setCam(30)
        self.cup = False