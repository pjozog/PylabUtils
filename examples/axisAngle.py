#!/usr/bin/env python

from pylab import *

import PylabUtils as plu

n1 = randn (3,)
n2 = array ([0, 0, 1])

axis, angle = plu.coord_xfms.axisang (n1, n2)

R = plu.coord_xfms.axisang2rot (axis, [angle])

print 'det: %f' % det (R)
print
print 'rotated: '
print R.dot (n1)
print n2
print 
print 'rotated/normalized: '
print R.dot (n1) / norm (R.dot (n1))
print n2 / norm (n2)
