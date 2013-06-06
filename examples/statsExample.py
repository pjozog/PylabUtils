#!/usr/bin/env python

from pylab import *
import PylabUtils as pylabu

import scipy.stats

N = 500
mu = array ([2, 2])
Sigma = pylabu.stats.randcov (2)
x = pylabu.stats.mvnrnd (mu, Sigma, N)

k2 = scipy.stats.chi2.ppf (.999, 2)
ellX, ellY = pylabu.plotting.calculateEllipseXY (mu, Sigma, k2, 50)
plt = figure ().add_subplot (111)
sh = plt.scatter (x[0,:], x[1,:], c=x[1,:])
plt.hold ('on')
lh = plt.plot (ellX, ellY)
ch = colorbar (sh)

ch.set_label ('Y value')
grid ('on')
axis ('equal')

show ()
