import numpy as np
from math import sin, cos, atan
import scipy.optimize
from time import time
import random

r1 = 10
r2 = 7
r3 = 5

constraints = {'a1': [-100, 100], 'a2': [-80, 80], 'a3':[-80,80]}

def f(a1, a2, a3):
    return r1*sin(a1) + r2*sin(a2) + r3*sin(a3), r1*cos(a1) + r2*cos(a2) + r3*cos(a3)
    
def get_angles(x, y):
    a1, a2, a3 = 0, 0, 0
    xc, yc = f(a1, a2, a3)
    while abs(xc-x) > 1e-2 or abs(yc-y) > 1e-2:
        rp_angle = atan(y/x)
        if constraints['a1'][0] > rp_angle:
            a1 = constrains['a1'][0] + 5
        elif constraints['a1'][1] < rp_angle:
            a1 = constrains['a1'][1] - 5
        else:
            a1 = random.randint(int(max(rp_angle - 20, constraints['a1'][0])), int(rp_angle))
        def F(x_in):
            temp = [r1*sin(a1) + r2*sin(x_in[0]) + r3*sin(x_in[1]) - x, r1*cos(a1) + r2*cos(x_in[0]) + r3*cos(x_in[1]) - y]
            return temp
            
        a2, a3 = scipy.optimize.fsolve(F, [1,1], xtol=1e-4)
        xc, yc = f(a1, a2, a3)
    
    return a1, a2, a3
   
t = time()
for _ in range(100):
    a1, a2, a3 = get_angles(10.0, 5.0)
    print(f(a1,a2,a3))
    print(a1, a2, a3)
print(time()-t)