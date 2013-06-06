#!/usr/bin/env python2

from pylab import *

from xyzrph2matrix import xyzrph2matrix
from matrix2xyzrph import matrix2xyzrph

from .. import diff

def ssc_inverse (x_ij):

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

def ssc_inverse_jacob (x_ij):
    return diff.numerical_jacobian (ssc_inverse, x_ij)
