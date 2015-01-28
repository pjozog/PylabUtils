#!/usr/bin/env python

import numpy as np
from pylab import find

def border (tri, inds=None):
    """

    Compute the line segments that constitute the border (inside and outside) of the triangulation 'tri'
    
    """
    edgeX = []
    edgeY = []

    if inds is None:
        inds = range (tri.simplices.shape[0])

    for ind in inds:
        neighbors = tri.neighbors[ind, :]
        if -1 in neighbors:
            pointIndsOppositeOutsideEdge = find (neighbors == -1)
            for pointIndOppositeOutsideEdge in pointIndsOppositeOutsideEdge:
                triangInds = tri.simplices[ind, :]
                outsideEdgeInds = np.delete (triangInds, pointIndOppositeOutsideEdge)
                edgeX.append (tri.points[outsideEdgeInds, :][:,0])
                edgeY.append (tri.points[outsideEdgeInds, :][:,1])
    return (edgeX, edgeY)
