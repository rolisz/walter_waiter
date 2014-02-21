#! /usr/bin/python
import event
import nxt.locator
import nxt.motor as motor
brick = nxt.locator.find_one_brick()
height_motor = motor.Motor(brick, motor.PORT_A)
height_motor.turn(127, 5000, brake=False)