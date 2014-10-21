#!/usr/bin/env python

from pylab import *
import PylabUtils as plu

fx, fy = (1000, 1000)
cx, cy = (1360/2, 1024/2)

x_w1 = zeros (6,)
x_w2 = .1 * rand (6,)
x_w3 = .1 * rand (6,)

K = array ([[fx, 0, cx],
            [0, fy, cy],
            [0, 0, 1.]])
cam1 = plu.cv.Camera (x_w1, K)
cam2 = plu.cv.Camera (x_w2, K)
cam3 = plu.cv.Camera (x_w3, K)

cams = [cam1, cam2, cam3]

uv = zeros ((2*len (cams),2))
XTrue = array ([[.2, -.3, 2],[-.2,-.3,1.5]]).T
uv[0:2,0:2] = cam1.project (XTrue)
uv[2:4,0:2] = cam2.project (XTrue)
uv[4:6,0:2] = cam3.project (XTrue)

X = plu.cv.dlt.triangulate (uv, cams)

print 'Measured feature locations:'
print uv

print 'True 3D points:'
print XTrue

print 'Predicted 3D points:'
print X
