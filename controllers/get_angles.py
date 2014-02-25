import numpy as np
from math import sin, cos, sqrt, pi, radians
import scipy.optimize
from time import time
import random

r1 = 121
r2 = 125
r3 = 150

delta = -2
constraints = {
    'a1': [radians(-85), radians(77)],
    'a2': [radians(-90), radians(30)],
    'a3': [radians(-77), radians(62)]
}


def f(a1, a2, a3):
    # X is the direction in front
    a2 = delta - a2
    return (r1*cos(a1) + r2*cos(a1+a2) + r3*cos(a1+a2+a3),
            r1*sin(a1) + r2*sin(a1+a2) + r3*sin(a1+a2+a3))


def get_angles(x, y):
    a1, a2, a3 = (0, 0, 1)

    def F(args):
        a1, a2, a3 = args
        xhat, yhat = f(a1, a2, a3)
        dist = sqrt((xhat-x)**2 + (yhat-y)**2)
        return dist

    res = scipy.optimize.minimize(F, [a1, a2, a3],
                                  tol=1e-3,
                                  method='TNC',
                                  bounds=[constraints[el] for el in ('a1',
                                                                     'a2',
                                                                     'a3')]
                                  )
    a1, a2, a3 = res['x']
    xc, yc = f(a1, a2, a3)

    print res
    return a1*180/pi, a2*180/pi, a3*180/pi

def angleToStartPos(v):
	"""
		A series of transformations of the forms
		't' - translation: go forward for a number of units
		'r' - rotation: rotate trigonometric wise a number of degrees
		are made on the (0, 0) coordinates. 
		We need to do a rotation so that the final position
		(x', y') will "face" the starting position (0, 0).
		Returns the degrees to rotate trigonometric wise
		so that we face the starting position.
		
		>>> '%.2f' % angleToStartPos([('r', 32)])
		'0.00'
		>>> '%.2f' % angleToStartPos([('t', 1)])
		'180.00'
		>>> '%.2f' % angleToStartPos([('t', 1), ('r', 90), ('t', 1)])
		'135.00'
		>>> '%.2f' % angleToStartPos([('t', 1), ('r', 45), ('r', 45), ('t', 1), ('r', 90), ('t', 2)])
		'135.00'
	"""
	theta = math.pi / 2
	x, y = 0, 0
	for t in v:
		if t[0] == 'r':
			theta = (theta + math.radians(t[1])) % (2 * math.pi)
		if t[0] == 't':
			x = x + t[1] * math.cos(theta)
			y = y + t[1] * math.sin(theta)

	if x == 0 and y == 0:
		return 0
	else:
		alpha = math.atan2(y, x)
		return math.degrees((-theta + alpha - math.pi) % (2 * math.pi))
