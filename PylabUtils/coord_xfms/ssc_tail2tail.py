#!/usr/bin/env python2

from pylab import *

from ssc_head2tail import ssc_head2tail
from ssc_inverse import ssc_inverse

from .. import diff

def ssc_tail2tail (x_gi, x_gj):
    return ssc_head2tail (ssc_inverse (x_gi), x_gj)

def ssc_tail2tail_jacob (x_gi, x_gj):
    x = concatenate ((x_gi, x_gj))
    return diff.numerical_jacobian (_f, x)

def _f (x):
    x_gi = x[0:6]
    x_gj = x[6:]
    return ssc_tail2tail (x_gi, x_gj)
