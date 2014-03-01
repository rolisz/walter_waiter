from get_angles import get_angles
import event


class CupState(event.DecisionMaker):

    def __init__(self, ev, lynx, nxt, cam_angle=-30):
        self.cam_angle = cam_angle
        self.ev = ev
        self.l = lynx
        self.nxt = nxt
        self.cups_got = 0
        self.cup = False
        self.init_angles = (77, 20, 62)
        super(CupState, self).__init__(ev)

    def run(self):
        # Move to initial position
        self.l.setAngles(*self.init_angles)
        self.nxt.release()
        super(CupState, self).run()

    def cup_start(self, _):
        self.l.setAngles(*self.init_angles)
        self.l.setCam(self.cam_angle)
        self.cups_got = 0
        self.cup = False

    def cup_appeared(self, coords):
        if self.cup:
            return
        else:
            self.cup = True
        angles = get_angles(coords[0]-10, -coords[1]+50)
        self.l.setAngles(*angles)  # shouldn't there be a time here as well?
        self.sleep(1)
        self.nxt.grasp()
        self.nxt.moveUp()
        self.moveOnTray()

    def moveOnTray(self):
        # Positions for cups, in the order to avoid collisions
        positions = [(-20, -270),
                     (80, -200) # TODO: test
                     ]

        cup_pos = positions[self.cups_got]
        a, b, c = get_angles(*cup_pos)
        self.l.setAngles(*self.init_angles)
        self.sleep(2)
        self.l.setAngles(a, b, c, time=2)
        self.sleep(2)
        self.nxt.moveDown()
        self.nxt.release()
        self.cup_released()

    def cup_released(self):
        self.cups_got += 1
        self.l.setAngles(*self.init_angles)
        self.sleep(1)
        if self.cups_got == 2:
            self.ev.unregister(event='frame', name='cd')
            self.sleep(0)
            self.ev.register(event='frame', name='fd')
            print 'emitting cups_done' # TODO: Haven't checked if this runs!!!
            self.emit('cups_done')
            self.l.setCam(30)
        self.cup = False
