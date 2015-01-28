#!/usr/bin/env python

import PylabUtils as plu
import pylab
from scipy.spatial import Delaunay

points = pylab.rand (200, 2)

# plot the raw points
pylab.figure ()
pylab.scatter (points[:,0], points[:,1])

# compute and show the triangulated points
tri = Delaunay (points)
pylab.figure ()
pylab.triplot(points[:,0], points[:,1], tri.simplices.copy())
pylab.plot(points[:,0], points[:,1], 'o')

# compute and show the alpha-shape
alphaInds = plu.triang.alphaShape (tri, alpha=0.2, removeNeighbors=True)
pylab.figure ()
pylab.triplot(points[:,0], points[:,1], tri.simplices[alphaInds, :].copy())
pylab.plot(points[:,0], points[:,1], 'o')

# compute and show the border ("concave hull")
(edgeX, edgeY) = plu.triang.border (tri, inds=alphaInds)
pylab.figure ()
pylab.scatter (points[:,0], points[:,1])
plu.plotting.plotLines (edgeX, edgeY, 'r')
pylab.show ()
