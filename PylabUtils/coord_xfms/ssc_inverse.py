#!/usr/bin/env python2

from pylab import *

from xyzrph2matrix import xyzrph2matrix
from matrix2xyzrph import matrix2xyzrph

from .. import diff

def ssc.inverse (x_ij):
    """

    Given the 6-DOF pose x_ij, return x_ji
    
    """

    Hij = xyzrph2matrix (x_ij)
    Rji = Hij[0:3, 0:3]
    tij = Hij[0:3,3]
    Rij = Rji.transpose ()
    tji = -Rij.dot (tij)
    Hji = zeros ((4,4))
    Hji[0:3,0:3] = Rij
    Hji[0:3,3] = tji
    Hji[3,3] = 1
    return matrix2xyzrph (Hji)

def ssc.inverse_jacob (x_ij):
    """

    Return the Jacobian of ssc.inverse
    
    """
    return diff.numerical_jacobian (ssc.inverse, x_ij)
