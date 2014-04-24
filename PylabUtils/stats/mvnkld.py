#!/usr/bin/env python

import pylab as pl

import numpy.linalg as linalg
from numpy import trace

def mvnkld (mu0, mu1, sigma0, sigma1):
    k = len (mu0)
    assert k == len (mu1)
    delta = mu1 - mu0
    lndet = pl.np.log (linalg.det (sigma0) / linalg.det (sigma1))
    return 0.5 * (trace (linalg.inv (sigma1).dot (sigma0)) + delta.T.dot (sigma1).dot (delta) - k + lndet)
