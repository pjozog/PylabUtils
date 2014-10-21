#!/usr/bin/env python

import pylab

def randcov (n):
    """
    
    Generates a random, but valid, covariance matrix (size nxn)

    """
    L = pylab.randn (n, n)
    D = pylab.eye (n)
    return L.T.dot (D).dot (L)
