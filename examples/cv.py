#!/usr/bin/env python

from pylab import *
import PylabUtils as plu

if __name__ == '__main__':
    xPrime = array ([[-1, 1, 1],
                 [1, 1, 1],
                 [1, -1, 1],
                 [-1, -1, 1]]).T

    x = array ([[0, 0, 1],
                [640, 0, 1],
                [640, 480, 1],
                [0, 480, 1]]).T

    H = plu.cv.dlt.homog2D (xPrime, x)

    print "Homography from DLT: "
    print H

    print plu.cv.dehomogenize (x)
    transformed = H.dot (x)
    print "       ^"
    print "       |"
    print "       |"
    print "       v"
    print plu.cv.dehomogenize (transformed)
