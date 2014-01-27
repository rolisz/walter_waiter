# -*- coding: utf-8 -*-
"""
Use the pixel coordinates and camera characteristics to
find the 3-d coordinates of the cup
Warning: doesn't use spherical coordinates:
    alpha is measured from the optical axis, not from the vertical one

Created on Sat Jan 25 12:36:14 2014

@author: dan
"""

import math

def get_angle_from_pixels(x_px, axis_size=640, axis_fov = 60.0):
    '''
    Gets the angle from the image coordinates
    Assumes pixels are linearly proportional to angle
    Horizontal FOV / vertical FOV ∈ {4/3, 16/9}
    
    >>> get_angle_from_pixels(0, 640, 60)
    -30.0
    
    >>> get_angle_from_pixels(640, 640, 60)
    30.0
    
    >>> get_angle_from_pixels(320, 640, 60)
    0.0
    '''
    
    # Linear function may err ~10 pixels (1/64 of resolution)
    # according to Blender experiment (coords.ods)
    return (x_px/float(axis_size) - 0.5) * axis_fov


def get_distance_from_cup_width(cup_width_px, axis_width=640, axis_fov=60):
    '''
    Custom function to detect the distance cup (in mm)
    Axis FOV is ignored, we only have data for our camera
    
    >>> '%.5f'% get_distance_from_cup_width(363.4)
    '205.10687'
    
    >>> '%.5f'% get_distance_from_cup_width(92)
    '845.43274'
    
    >>> '%.5f'% get_distance_from_cup_width(46, 320)
    '845.43274'
    
    >>> '%.5f'% get_distance_from_cup_width(92, 320, 30)
    '845.43274'
    
    '''
    
    return 78.0/math.tan(cup_width_px*(0.64/axis_width) * (axis_fov/60.0))
    
def get_coords(distance, x_angle, y_angle):
    '''
    Convert almost-spherical coordinates to Cartesian ones
    
    @param distance:
        Distance from origin of camera to point
    @param x_angle:
        Angle between camera's optical axis and point
        projected to horizontal plane
    @param y_angle:
        Angle between camera's optical axis and point
        projected on a horizontal plane
        NOTE: on Wikipedia, this angle is from vertical axis
        This is why we switch sin with cos on theta
    
    >>> '%.2f %.2f %.2f' % get_coords(8, 25, 0)
    '7.25 3.38 0.00'
    
    >>> '%.2f %.2f %.2f' % get_coords(11, 15, -15)
    '10.26 2.75 -2.85'
    
    '''
    theta = float(y_angle) * math.pi/180.0
    psi =  float(x_angle) * math.pi/180.0
    r = float(distance)

    x = r * math.cos(theta) * math.cos(psi)
    y = r * math.cos(theta) * math.sin(psi)
    z = r * math.sin(theta)
    
    return (x, y, z)

def pixels2coords(x_px, y_px, cup_width_px, size=(480,640), hfov=60):
    '''
    Convert pixel coordinates to our cup's position
    
    >>> '%.2f %.2f %.2f' % pixels2coords(320, 240, 298)
    '253.95 0.00 0.00'
    
    >>> '%.2f %.2f %.2f' % pixels2coords(0, 240, 149, hfov=120)
    '253.95 0.00 0.00'
    
    '''
    
    #TODO: test!!!
    distance = get_distance_from_cup_width(cup_width_px, size[1], hfov)
    x_angle = get_angle_from_pixels(x_px, size[1], hfov)
    # We assume pixels are square:
    y_angle = get_angle_from_pixels(y_px, size[0], hfov*size[0]/float(size[1]))
    return get_coords(distance, x_angle, y_angle)
    
# Run the file to test
import doctest
fails, _ = doctest.testmod()#raise_on_error=True)
if fails == 0:
    print '[OK] pixel2coords'