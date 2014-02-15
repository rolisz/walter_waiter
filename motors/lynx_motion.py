from ssc32 import *
from time import sleep
from smooth import getPositions
# Run with sudo


class Arm:
    def __init__(self, usb='/dev/ttyUSB0'):
        self.ssc = SSC32(usb, 115200)
        self.ssc[0].degrees = 20
        self.ssc[0].max = 2500
        self.ssc[0].min = 500
        self.ssc[0].deg_max = +90.0
        self.ssc[0].deg_min = -90.0

    #TODO: fix library so it doesn't take 100ms for the first instruction
    # And which overrides the current command even if it has the same
    # targetDegs

    def moveTo(self, motor, mi, time, targetDegs, dryRun=True):
        currDegs = motor[mi].degrees
        motor[mi].degrees = targetDegs
        print time, motor[mi].degrees
        if not dryRun:
            motor.commit(time*1000)
        print("moved")

    def smoothMoveTo(self, motor, mi, time, targetDegs, dryRun=True):
        freq = 100.0
        timePerStep = time/freq
        currDegs = motor[mi].degrees
        distToGo = targetDegs - currDegs
        for pos in getPositions(currDegs, targetDegs, freq):
            self.moveTo(motor, mi, timePerStep, pos, dryRun)

    def setAngles(self, v0, v1, v2, time=1):
        vals = [v0, v1, v2]

        for motor, degree in enumerate(vals):
            # if motor == 1:
            #     degree *= -1
            #     degree += 50
            self.moveTo(self.ssc, motor, time, degree, False)
            #sleep(0.1)

    def setCam(self, angle):
        self.ssc[3].degrees = angle
        self.ssc.commit(1000)
