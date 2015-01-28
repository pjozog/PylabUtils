#!/usr/bin/env python

from scipy.spatial.distance import pdist
import numpy as np

def circumradius (vertices):
    """
    Compute the circumradius of the triangle given by 'vertices', which is a 3x2 array
    of a triangle's vertices

    """
    assert (vertices.shape == (3,2))
    dists = pdist (vertices)
    R = dists.prod () / (np.sqrt (dists.sum () * (dists[1] + dists[2] - dists[0])\
                               * (dists[2] + dists[0] - dists[1])\
                               * (dists[0] + dists[1] - dists[2])))
    return R
