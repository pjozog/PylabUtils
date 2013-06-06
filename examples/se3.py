#!/usr/bin/env python

from pylab import *
from mpl_toolkits.mplot3d import Axes3D

import PylabUtils as pylabu

fig = figure ()
ax = fig.add_subplot (111, projection='3d')
pylabu.plotting.plot_coordinate_frame (pylabu.coord_xfms.rotxyz ( 0, .0, 0), [0, 0, 0], axis=ax, label='0')
hold ('on')
pylabu.plotting.plot_coordinate_frame (pylabu.coord_xfms.rotxyz (.1, .2, .3), [.1, .2, .3], axis=ax, label='1')

points = pylabu.stats.mvnrnd (array ([0,0,5]), .1 * eye(3), 100)
ax.plot (points[0,:], points[1,:], points[2,:], '.')

show ()
