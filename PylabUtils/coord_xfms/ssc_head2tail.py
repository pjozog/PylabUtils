#!/usr/bin/env python2

from pylab import *

from xyzrph2matrix import xyzrph2matrix
from matrix2xyzrph import matrix2xyzrph

from .. import diff

def ssc_head2tail (x_ij, x_jk):
    """
    
    Given 6-DOF pose arrays x_ij and x_jk, return x_ik

    """
    Hij = xyzrph2matrix (x_ij)
    Hjk = xyzrph2matrix (x_jk)
    Hik = Hij.dot (Hjk)
    x_ik = matrix2xyzrph (Hik)
    return x_ik

def ssc_head2tail_jacob (x_ij, x_jk):
    """
    
    Returns the Jacobian of ssc_head2tail

    """
    x = concatenate ((x_ij, x_jk))
    return diff.numerical_jacobian (_f, x)

def _f (x):
    x_ij = x[0:6]
    x_jk = x[6:]
    return ssc_head2tail (x_ij, x_jk)
