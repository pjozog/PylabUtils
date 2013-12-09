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
    print 'x_i:'
    print plu.cv.dehomogenize (x)
    transformed = H.dot (x)
    print 'H * x_i:'
    print plu.cv.dehomogenize (transformed)

    fx, fy = (1772.074719488086, 1775.368219152238)
    cx, cy = (639.0952186799014, 609.3077173645565)

    x_wc = array ([-.2, .3, 4, -.1, .3, -.05])
    K = array ([[fx, 0, cx, 0. ],
                [0, fy, cy, 0. ],
                [0, 0, 1., 0.]])
    cam = plu.cv.Camera (x_wc, K)

    # uv = array ([453., 123.])
    uv1 = array ([453., 123.])
    uv2 = array ([872., 631.])
    uv = column_stack ((uv1, uv2))

    lam = 1.
    Xtrace = cam.raytrace (uv, lam)
    print 
    print 'Camera pose in world frame:'
    print x_wc
    print 'Observed point in image plane:'
    print uv
    print 'Back-projected 3D point in camera frame (lambda=%f):' % lam
    print Xtrace
    print 'Corresponding forward-projected image point'
    print cam.project (Xtrace)
