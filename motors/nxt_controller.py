import nxt.locator
import nxt.motor as motor
import nxt.sensor as sensor


class NxtController():
    def __init__(self):
        self.brick = nxt.locator.find_one_brick()
        self.motor = motor.Motor(self.brick, motor.PORT_B)
        self.height_motor = motor.Motor(self.brick, motor.PORT_A)
        self.obstacle_detector = sensor.Ultrasonic(self.brick, sensor.PORT_1)

    def moveUp(self, value=2000):
        self.height_motor.turn(-127, value, brake=False)

    def moveDown(self, value=2000):
        self.height_motor.turn(127, value, brake=False)

    def grasp(self):
        try:
            self.motor.turn(-10, 200)
        except motor.BlockedException as e:
            self.motor.brake()

    def release(self):
        try:
            self.motor.turn(10, 200)
        except motor.BlockedException as e:
            self.motor.brake()

    def getObstacleDistance(self):
        return self.obstacle_detector.get_distance()
