import event
import nxt.locator
import nxt.motor as motor


class NxtController(event.DecisionMaker):
    def __init__(self, ev):
        self.brick = nxt.locator.find_one_brick()
        self.motor = motor.Motor(self.brick, motor.PORT_B)
        try:
            self.motor.turn(10, 200)
        except:
            pass
        super(NxtController, self).__init__(ev)

    def run(self):
        while True:
            event, value = self.queue.get(True, 20000)
            print(event)
            if event == 'arm_aligned':
                try:
                    print('turning')
                    self.motor.turn(-10, 200)
                    print('turned')
                except Exception:
                    print('excepted')
                    self.emit('cup_grasped', True)
                    self.motor.brake()
            if event == 'cup_over_tray':
                try:
                    self.motor.turn(10, 400)
                except Exception:
                    self.motor.idle()
                    self.emit('cup_released', True)

