#!/usr/bin/env python

import sys, os

import mayavi.mlab
import numpy
from pylab import *

import PylabUtils as plu

DATA = '3d-points'

N = 100
R = .001 * eye (3)
mu = array([1,2,3])
if os.path.exists (DATA):
    X = numpy.loadtxt (DATA)
else:
    X = plu.stats.mvnrnd (mu, R, N)

X = zeros ((3, N))
X[0,0:N/2] = -0.5
X[0,N/2:] = 0.5

X[1,0:N/2] = linspace (-1.5, 1.5, N/2)
X[1,N/2:] = linspace (-1.5, 1.5, N/2)

X += plu.stats.mvnrnd (array([0,0,-1]), R, N)

S = cov (X)
W, V = eig (S)
n = V[:,argmin (W)]

mu = mean (X, 1)

fig = mayavi.mlab.figure (fgcolor=(0,0,0), bgcolor=(1,1,1))
plu.plotting.mayavi_plot_coordinate_frame (plu.coord_xfms.rotxyz (rand (), rand (), rand ()), zeros (3,))
mayavi.mlab.points3d (X[0,:], X[1,:], X[2,:], scale_factor=0.05)
mayavi.mlab.outline ()
mayavi.mlab.axes ()
# mayavi.mlab.plot3d ([mu[0], mu[0]+n[0]], [mu[1], mu[1]+n[1]], [mu[2], mu[2]+n[2]])
mayavi.mlab.quiver3d (mu[0], mu[1], mu[2], n[0], n[1], n[2], line_width=5, mode='arrow', color=(0,0,0))
# mayavi.mlab.show ()
