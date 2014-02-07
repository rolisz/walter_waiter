#!/usr/bin/env python

# Requires the Fedora packages nxt_python and nbc

import nxt.locator
from nxt.motor import *

def spin_around(b, port, position):
        motorFinger = Motor(b, port)
	motorFinger.turn(-30, 100)
'''        
	print(b)
        print(motorFinger)
        currentTacho = motorFinger.get_tacho()
        currentTacho = currentTacho.rotation_count
        sign = 1;
        diff = position - currentTacho
        if diff < 0:
                sign = -1
        speed = 10
        diff = abs(diff)
        motorFinger.turn(sign * speed, diff)
        #print diff, currentTacho
'''

b = nxt.locator.find_one_brick()
tachoOpenFinger = 1900
tachoClosedFinger = 1780

#spin_around(b, tachoOpenFinger)
spin_around(b, PORT_B, tachoClosedFinger)
spin_around(b, PORT_B, tachoOpenFinger)

