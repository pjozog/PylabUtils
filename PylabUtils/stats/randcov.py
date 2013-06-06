#!/usr/bin/env python

from pylab import *

def randcov (n):

    L = randn (n, n)
    D = eye (n)
    return L.transpose ().dot (D).dot (L)
