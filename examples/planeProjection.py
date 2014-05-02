#!/usr/bin/env python

from pylab import *

import PylabUtils as plu

# camera frame denoted as 'c'

x_wc = array ([0.1, -0.3, 2, 0.1, -0.1, 0.2])
print 'Camera pose in world coordinates:'
print x_wc
print

K = array ([[1686.272391850991, 0, 678.9042146410625],
            [0, 1680.081185613841, 545.8653337768013],
            [0, 0, 1]])
cam = plu.cv.Camera (x_wc, K)

# camera observed point on image plane (pixel coordinates)
uv = array ([400, 300])
print '2D point observed in image coordinates:'
print uv
print

# plane indexed as 'k'
pi_ck = plu.plane3d.Plane3d (1.0, -0.2, -1.0)
print "Plane normal in camera's frame:"
print pi_ck
print

X = cam.backprojectOnPlane (uv, pi_ck)
print '3D point in world coordinates: '
print X
print

Xcam = cam.transformPoints (X)
print '3D point in camera coordinates:'
print Xcam
print

uvPredicted = cam.project (X)
print 'Predicted 2D point in image coordinates:'
print uvPredicted
