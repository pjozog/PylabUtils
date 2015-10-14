import numpy
from numpy import concatenate

from xyzrph2matrix import xyzrph2matrix
from matrix2xyzrph import matrix2xyzrph

from .. import diff

def head2tail (x_ij, x_jk):
    """
    
    Given 6-DOF pose arrays x_ij and x_jk, return x_ik

    """
    Hij = xyzrph2matrix (x_ij)
    Hjk = xyzrph2matrix (x_jk)
    Hik = Hij.dot (Hjk)
    x_ik = matrix2xyzrph (Hik)
    return x_ik

def head2tail_jacob (x_ij, x_jk):
    """
    
    Returns the Jacobian of head2tail

    """
    x = concatenate ((x_ij, x_jk))
    return diff.numerical_jacobian (_fh2t, x)

def _fh2t (x):
    x_ij = x[0:6]
    x_jk = x[6:]
    return head2tail (x_ij, x_jk)

def inverse (x_ij):
    """

    Given the 6-DOF pose x_ij, return x_ji
    
    """

    Hij = xyzrph2matrix (x_ij)
    Rji = Hij[0:3, 0:3]
    tij = Hij[0:3,3]
    Rij = Rji.transpose ()
    tji = -Rij.dot (tij)
    Hji = numpy.zeros ((4,4))
    Hji[0:3,0:3] = Rij
    Hji[0:3,3] = tji
    Hji[3,3] = 1
    return matrix2xyzrph (Hji)

def inverse_jacob (x_ij):
    """

    Return the Jacobian of inverse
    
    """
    return diff.numerical_jacobian (inverse, x_ij)

def tail2tail (x_gi, x_gj):
    """

    Given 6-DOF poses x_gi and x_gj, return x_ij
    
    """

    return head2tail (inverse (x_gi), x_gj)

def tail2tail_jacob (x_gi, x_gj):
    """

    Return the Jacobian of tail2tail
    
    """
    x = concatenate ((x_gi, x_gj))
    return diff.numerical_jacobian (_ft2t, x)

def _ft2t (x):
    x_gi = x[0:6]
    x_gj = x[6:]
    return tail2tail (x_gi, x_gj)
