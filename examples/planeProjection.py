#!/usr/bin/env python

from pylab import *

import PylabUtils as plu

# camera frame denoted as 'c'

x_wc = rand (6,)
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

# rotate the plane so that it's the ground plane (0, 0, 1)
pi_ground = plu.plane3d.Plane3d (0, 0, 1)
R_grnd = pi_ck.rot (pi_ground)

# we now want to back-project a point onto the artificial ground plane

# rotate everything so that plane 'k' is the ground plane
rph = plu.coord_xfms.rot2rph (R_grnd)

# get new rotated reference frame (where all points on the original plane are [x y 0])
# "x_cnew" : "Transformation from camera frame to new frame"
x_cnew = array ([-pi_ck.x, -pi_ck.y, -pi_ck.z, rph[0], rph[1], rph[2]])
# "x_wnew" : "Transformation from world frame to new frame"
x_wnew = plu.coord_xfms.ssc_head2tail (x_wc, x_cnew)
# "x_newc" : "Transformation from new frame to camera frame"
x_newc = plu.coord_xfms.ssc_inverse (x_cnew)
camnew = plu.cv.Camera (x_newc, K)

# we know if we back-projected the 2D pixel point to 3D space in this new reference frame,
# it will have z coordinate of zero.  Therefore, discard the third column of camera
# projection matrix P
Preduced = camnew.P[:,[0, 1, 3]]

# now we can recover the X Y (and Z, since it's zero) of the 3D point in rotated reference frame
backproj = plu.cv.dehomogenize (inv (Preduced).dot (plu.cv.homogenize (uv)))
Xnew = array ([backproj[0], backproj[1], 0])

# transform back to original reference frame
H = plu.coord_xfms.xyzrph2matrix (x_wnew)
X = plu.cv.dehomogenize (H.dot (plu.cv.homogenize (Xnew)))
print '3D point in world coordinates: '
print X

uvPredicted = cam.project (X)
print 'Predicted 2D point in image coordinates:'
print uvPredicted
