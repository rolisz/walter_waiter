import event
import nxt.locator
import nxt.motor as motor



class NxtController(event.DecisionMaker):
    def __init__(self, ev):
        self.brick = nxt.locator.find_one_brick()
        self.motor = motor.Motor(self.brick, motor.PORT_B)
        self.height_motor = motor.Motor(self.brick, motor.PORT_A)
        try:
            self.motor.turn(10, 100)
        except:
            pass
        super(NxtController, self).__init__(ev)

    def arm_aligned(self, _):
        try:
            print('turning')
            self.motor.turn(-10, 150)

        except Exception:
            print('turned')
            self.height_motor.turn(-127, 5000, brake=False)
            self.emit('cup_grasped', True)
            self.motor.brake()

    def cup_over_tray(self, _):
        try:
            self.height_motor.turn(127, 5000, brake=False)
            self.motor.turn(10, 200)
        except Exception:

            print('turned')
            self.motor.idle()
            self.emit('cup_released', True)
