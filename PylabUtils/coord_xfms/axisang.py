#!/usr/bin/env python

from pylab import np

def axisang (n1, n2):
    """ Returns the axis/angle rotation (in radians) that rotates norms n1 to n2."""
    axis = np.cross (n1, n2)
    axisnorm = np.linalg.norm (axis)
    if not np.allclose (axisnorm, 0):
        axis = axis / axisnorm
    angle = np.arccos (n1.dot (n2) / (np.linalg.norm (n1) * np.linalg.norm (n2)))
    return axis, angle

def axisang2rot (axis, angle):
    """ Converts axis/angle rotation to a rotation matrix"""
    R = np.zeros ((3, 3))
    theta = angle

    R[0,0] = np.cos (theta) + (axis[0]**2) * (1 - np.cos (theta))
    R[0,1] = axis[0]*axis[1]*(1-np.cos (theta)) - axis[2]*np.sin (theta)
    R[0,2] = axis[0]*axis[2]*(1-np.cos (theta)) + axis[1]*np.sin (theta)

    R[1,0] = axis[1]*axis[0]*(1-np.cos (theta)) + axis[2]*np.sin (theta)
    R[1,1] = np.cos (theta) + (axis[1]**2) * (1 - np.cos (theta))
    R[1,2] = axis[1]*axis[2]*(1-np.cos (theta)) - axis[0]*np.sin (theta)

    R[2,0] = axis[2]*axis[0]*(1-np.cos (theta)) - axis[1]*np.sin (theta)
    R[2,1] = axis[2]*axis[1]*(1-np.cos (theta)) + axis[0]*np.sin (theta)
    R[2,2] = np.cos (theta) + (axis[2]**2)*(1-np.cos (theta))

    return R
