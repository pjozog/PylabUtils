#!/usr/bin/env python

from circumradius import circumradius

def alphaShape (tri, alpha, removeNeighbors=True):
    """
    
    Remove triangles in 2D triangulation 'tri' that have a circumradius less than alpha

    """
    numTriangs = tri.simplices.shape[0]
    alphaInds = []
    for triangInd in range (numTriangs):
        # compute the circumradius
        triangPoints = tri.points [tri.simplices[triangInd, :], :]
        if (circumradius (triangPoints) < alpha):
            alphaInds.append (triangInd)

    # remove triangles not in the alpha shape
    if removeNeighbors:
        for alphaInd in alphaInds:
            # compute the circumradius
            for i, neighbor in enumerate (tri.neighbors[alphaInd, :]):
                if neighbor not in alphaInds:
                    tri.neighbors[alphaInd,i] = -1
    
    return alphaInds
