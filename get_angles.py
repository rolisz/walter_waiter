import numpy as np
from math import sin, cos, atan, pi
import scipy.optimize
from time import time
import random

r1 = 120
r2 = 120
r3 = 150

constraints = {'a1': [-pi/2, pi/2], 'a2': [-pi/2, pi/2], 'a3':[-pi/2,pi/2]}

def f(a1, a2, a3):
    return r1*sin(a1) + r2*sin(a2) + r3*sin(a3), r1*cos(a1) + r2*cos(a2) + r3*cos(a3)
    
def get_angles(x, y):
    a1, a2, a3 = 0, 0, 0
    xc, yc = f(a1, a2, a3)
    i = 0
    while (abs(xc-x) > 1e-2 or abs(yc-y) > 1e-2) and i < 10:
        rp_angle = atan(y/x)
        if constraints['a1'][0] > rp_angle:
            a1 = constrains['a1'][0] + 0.03
        elif constraints['a1'][1] < rp_angle:
            a1 = constrains['a1'][1] - 0.03
        else:
            a1 = random.uniform(float(max(rp_angle - 0.12, constraints['a1'][0])), float(min(rp_angle + 0.12, constraints['a1'][1])))
        def F(x_in):
            temp = [r1*sin(a1) + r2*sin(x_in[0]) + r3*sin(x_in[1]) - x, r1*cos(a1) + r2*cos(x_in[0]) + r3*cos(x_in[1]) - y]
            return temp
            
        a2, a3 = scipy.optimize.fsolve(F, [1,1], xtol=1e-4)
        xc, yc = f(a1, a2, a3)
        i+=1
    if i == 10:
        print(a1,a2,a3, f(a1,a2,a3))
        raise Exception("No solution")
    return a1, a2, a3
   
t = time()
for _ in range(10):
    try:
        a1, a2, a3 = get_angles(240, 0)
        print(f(a1,a2,a3))
        print(a1*180/pi, a2*180/pi, a3*180/pi)
    except:
        print("No solution")
print(time()-t)