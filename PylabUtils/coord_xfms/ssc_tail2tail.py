#!/usr/bin/env python2

from pylab import *

from ssc.head2tail import ssc.head2tail
from ssc.inverse import ssc.inverse

from .. import diff

def ssc.tail2tail (x_gi, x_gj):
    """

    Given 6-DOF poses x_gi and x_gj, return x_ij
    
    """

    return ssc.head2tail (ssc.inverse (x_gi), x_gj)

def ssc.tail2tail_jacob (x_gi, x_gj):
    """

    Return the Jacobian of ssc.tail2tail
    
    """
    x = concatenate ((x_gi, x_gj))
    return diff.numerical_jacobian (_f, x)

def _f (x):
    x_gi = x[0:6]
    x_gj = x[6:]
    return ssc.tail2tail (x_gi, x_gj)
