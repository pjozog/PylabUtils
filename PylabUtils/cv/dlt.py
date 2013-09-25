#!/usr/bin/env python

import pylab as pl

def homog2D (xPrime, x):
    """
    
    Compute the 3x3 homography matrix mapping a set of N 2D homogeneous 
    points (3xN) to another set (3xN)

    """

    numPoints = xPrime.shape[1]
    assert (numPoints >= 4)

    A = None
    for i in range (0, numPoints):
        xiPrime = xPrime[:,i]
        xi = x[:,i]

        Ai_row0 = pl.concatenate ((pl.zeros (3,), -xiPrime[2]*xi, xiPrime[1]*xi))
        Ai_row1 = pl.concatenate ((xiPrime[2]*xi, pl.zeros (3,), -xiPrime[0]*xi))
        Ai = pl.row_stack ((Ai_row0, Ai_row1))

        if A is None:
            A = Ai
        else:
            A = pl.vstack ((A, Ai))

    U, S, V = pl.svd (A)
    V = V.T
    h = V[:,-1]
    H = pl.reshape (h, (3, 3))
    return H
