#!/usr/bin/env python

import pylab as pl
from .skewsym import skewsym
from . import homogeneous
from .. import coord_xfms

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

def homog3D (points2d, points3d):
    """

    Compute a matrix relating homogeneous 3D points (4xN) to homogeneous
    2D points (3xN)

    Not sure why anyone would do this.  Note that the returned transformation
    *NOT* an isometry.  But it's here... so deal with it.

    """

    numPoints = points2d.shape[1]
    assert (numPoints >= 4)

    A = None
    for i in range (0, numPoints):
        xiPrime = points2d[:,i]
        xi = points3d[:,i]

        Ai_row0 = pl.concatenate ((pl.zeros (4,), -xiPrime[2]*xi, xiPrime[1]*xi))
        Ai_row1 = pl.concatenate ((xiPrime[2]*xi, pl.zeros (4,), -xiPrime[0]*xi))
        Ai = pl.row_stack ((Ai_row0, Ai_row1))

        if A is None:
            A = Ai
        else:
            A = pl.vstack ((A, Ai))

    U, S, V = pl.svd (A)
    V = V.T
    h = V[:,-1]
    P = pl.reshape (h, (3, 4))
    return P

def triangulate (points2d, cameras):
    """

    Compute the N-view triangulation of corresponding 2D image points, given calibrated camera poses

    points2d: 2N-by-M matrix of 2D image points  (N: number of cameras, M: number of image points)
    cameras: length-N list of Camera objects

    """

    N = len (cameras)
    M = points2d.shape[1]

    pointsNorm = pl.zeros (points2d.shape)

    for camInd, camera in enumerate (cameras):
        points = points2d[camInd*2:(camInd*2)+2,:]
        pointsNorm[camInd*2:(camInd*2)+2,:] = camera.normalize (points)

    X = pl.zeros ((3,M))
    for pointInd in range (M):
        A = pl.zeros ((3*N,4))
        AStartRow = 0
        skewsyms = pl.zeros ((3,3,N))

        for camInd, camera in enumerate (cameras):
            skewsyms[:,:,camInd] = skewsym (homogeneous.homogenize (pointsNorm[camInd*2:(camInd*2)+2,pointInd]))
            A[AStartRow:AStartRow+3, 0:4] = skewsyms[:,:,camInd].dot (camera.wHc[0:3,0:4])
            AStartRow += 3

        U, S, VT = pl.svd (A)
        V = VT.T

        X[:,pointInd] = homogeneous.dehomogenize (V[:,-1])

    return X
