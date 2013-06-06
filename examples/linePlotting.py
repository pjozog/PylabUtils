#!/usr/bin/env python

import os, sys

from pylab import *
import PylabUtils as pylabu
import scipy.stats
import scipy.stats

x = linspace (-20,20, 100)
y = sin (x) / x
ax = pylabu.plotting.LinePlot (x, y).newAx ()
handle1 = ax.plot (x, y)

show ()
