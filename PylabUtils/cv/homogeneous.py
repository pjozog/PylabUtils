#!/usr/bin/env python

from pylab import *

def homogenize (points):
    """

    Copy to a homogenious array of points
    
    """

    if len (points.shape) == 1:
        return hstack ([points, ones (1,)])
    else:
        return row_stack ([points, ones (points.shape[1])])

def dehomogenize (points):
    """

    Convert to dehomogenious vectors, copying data
    
    """
    pointsCp = copy (points)
    if len (points.shape) == 1:
        pointsCp = pointsCp / pointsCp[-1]
        return pointsCp[0:-1]
    else:
        for row in range (0, points.shape[0]):
            pointsCp[row,:] = pointsCp[row,:] / pointsCp[-1,:]
        pointsCp = delete (pointsCp, -1, 0)
        return pointsCp
