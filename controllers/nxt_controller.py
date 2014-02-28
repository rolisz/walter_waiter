import event
import nxt.locator
import nxt.motor as motor
import nxt.sensor as sensor



class NxtController(event.DecisionMaker):
    def __init__(self, ev):
        self.brick = nxt.locator.find_one_brick()
        self.motor = motor.Motor(self.brick, motor.PORT_B)
        self.height_motor = motor.Motor(self.brick, motor.PORT_A)
        self.obstacle_detector = sensor.Ultrasonic(self.brick, sensor.PORT_1)
        super(NxtController, self).__init__(ev)


    def run(self):
        try:
            self.motor.turn(10, 100)
        except Exception as e:
            print 'Exception in nxt_controller: ', str(e)
            pass
        print "trying to run"
        super(NxtController, self).run()


    def arm_aligned(self, _):
        try:
            self.motor.turn(-10, 200)
        except motor.BlockedException:
            # Move up
            self.height_motor.turn(-127, 5000, brake=False)
            self.emit('cup_grasped', True)
            self.motor.brake()

    def cup_over_tray(self, _):
        try:
            # Move down
            self.height_motor.turn(127, 5000, brake=False)
            self.motor.turn(10, 200)
        except motor.BlockedException:
            self.motor.idle()
            self.emit('cup_released', True)
            return
        self.emit('cup_released', True)

    def obstacle_distance(self, _):
        distance = self.obstacle_detector.get_distance()
        self.emit('obstacle', distance)
