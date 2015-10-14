#!/usr/bin/env python

import os, sys

from pylab import *
import PylabUtils as pylabu

import scipy.stats
import scipy.stats

x = linspace (-6,6, 100)
y = linspace (-6,6, 100)
xx, yy = meshgrid (x, y)
r = 1
zz = sqrt (xx**2 + yy**2) < r
ax = pylabu.plotting.ImagePlot (zz).newAx ()
handle1 = ax.imshow (zz, interpolation='none')

zzFft = fftshift (abs (fft2 (zz)))
ax2 = pylabu.plotting.ImagePlot (zzFft).newAx ()
handle2 = ax2.imshow (zzFft, interpolation='none')
colorbar (handle2)

filename = '/usr/local/lib/python2.7/dist-packages/matplotlib/mpl-data/sample_data/Minduka_Present_Blue_Pack.png'
if not os.path.exists (filename):
    filename = '/usr/share/matplotlib/sampledata/Minduka_Present_Blue_Pack.png'
i = pylabu.image_processing.rgb2gray (imread (filename))
ax3 = pylabu.plotting.ImagePlot (i).newAx ()
handle3 = ax3.imshow (i)
ax3.hold ('on')
ax3.plot (i.shape[0]/2, i.shape[1]/2, 'ro')
handle3.set_cmap (cm.gray)
colorbar (handle3)

show ()
