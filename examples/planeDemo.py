#!/usr/bin/env python

import sys, os

import mayavi.mlab
import numpy
from pylab import *

import PylabUtils as plu

def fitPlane (points):
    mu = mean (points, 1)
    N = points.shape[1]
    U, S, Vt = svd (points - tile (mu, (N, 1)).T, full_matrices=False)
    V = Vt.T
    n = U[:,2]

    d = mu.dot (n)
    xyz = -d*n                  # line segment from origin to closest point on plane
    return plu.plane3d.Plane3d (xyz[0], xyz[1], xyz[2])

def plotPoints (points):
    mayavi.mlab.points3d (points[0,:], points[1,:], points[2,:], scale_factor=0.05)

def plotAxis (pose, **kwargs):
    R = plu.coord_xfms.rotxyz (pose[plu.coord_xfms.dofs.ROLL],
                               pose[plu.coord_xfms.dofs.PITCH],
                               pose[plu.coord_xfms.dofs.HEADING])
    t = pose[0:3]
    plu.plotting.mayavi_plot_coordinate_frame (R, t, **kwargs)

##
# assumes plane and pose are both in global frame
def plotPlane (plane, pose, color):
    shiftedPlane = plane.ominus (pose)

    p1 = zeros (3,)
    p2 = -array ([shiftedPlane.x, shiftedPlane.y, shiftedPlane.z])
    p = plu.cv.homogenize (column_stack ((p1, p2)))
    H = plu.coord_xfms.xyzrph2matrix (pose)
    p = H.dot (p)
    p = plu.cv.dehomogenize (p)

    p1 = p[:,0]
    p2 = p[:,1]
    n = -array ([(p2[0] - p1[0]), (p2[1] - p1[1]), (p2[2] - p1[2])])
    mayavi.mlab.quiver3d (p2[0], p2[1], p2[2],
                          n[0], n[1], n[2],
                          color=matplotlib.colors.ColorConverter.colors[color],
                          line_width=3.0,
                          mode='arrow',
                          scale_factor=1)

    # mayavi.mlab.plot3d (p[0,:], p[1,:], p[2,:],
    #                     color=matplotlib.colors.ColorConverter.colors[color],
    #                     tube_radius=0.025)

xyz = 3*rand (3,2)
rp = 2*pi * rand (2,2)
h = 2*pi * rand (1,2)

poses = vstack ((xyz, rp, h))

# points are in global frame
pointsMu = array ([4, 0, 0])
pointsSigma = diag ([0.01, 2, 2])
pointsSigma = diag ([0.01, 3, 3])
points = plu.stats.mvnrnd (pointsMu, pointsSigma, 1000)

plane = fitPlane (points)

fig = mayavi.mlab.figure (fgcolor=(0,0,0), bgcolor=(1,1,1))

# myPoints = array([[4, 4, 4, 4],
#                   [0, 4, 4, 0],
#                   [-3, -3, 3, -3]])
# mayavi.mlab.plot3d (myPoints[0,:], myPoints[1,:], myPoints[2,:])

plotPoints (points)
origin = array ([0, -2.8, 2.8, 0, 0, 0])
plotAxis (origin)
plotAxis (poses[:,0], color='rcc')
plotAxis (poses[:,1], color='rmm')
mayavi.mlab.axes (extent=[0,4,-3,3,-3,3])
plotPlane (plane, origin, 'k')
plotPlane (plane, poses[:,0], 'c')
plotPlane (plane, poses[:,1], 'm')

mayavi.mlab.view (azimuth=162.58073256326711,
                  elevation=108.87163479097813,
                  distance=26.466950118766441,
                  focalpoint=array([ 2.10151262,  0.28128219,  0.18349075]))

fig = mayavi.mlab.figure (fgcolor=(0,0,0), bgcolor=(1,1,1))
SIZE = 3
grid = array ([[0, 0, SIZE, SIZE, 0],
               [0, SIZE, SIZE, 0, 0],
               [0, 0, 0, 0, 0]])
grid = plu.cv.homogenize (grid)
x = 2*rand (6,)
H = plu.coord_xfms.xyzrph2matrix (x)
grid = H.dot (grid)
grid = plu.cv.dehomogenize (grid)

mayavi.mlab.plot3d (grid[0,:], grid[1,:], grid[2,:])

grid = grid[:,0:4]
mu = mean (grid, 1)
U, S, Vt = svd (grid - tile (mu, (4, 1)).T, full_matrices=False)
n = U[:,2]
mayavi.mlab.quiver3d (mu[0], mu[1], mu[2], n[0], n[1], n[2])

mayavi.mlab.show ()
