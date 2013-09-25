#!/usr/bin/env python

from pylab import find, unravel_index

def find2 (z):
    """

    2d version of find, returning row and column indeces that match the criteria 
    for the 2D array z

    Examples
    --------

    >>> A = array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
    >>> rowIdxs, colIdxs = find2 (A > 3)

    """
    inds = find (z)
    rowInds, colInds = unravel_index (inds, z.shape)
    return rowInds, colInds
