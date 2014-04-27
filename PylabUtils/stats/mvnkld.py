#!/usr/bin/env python

import pylab as pl

import numpy.linalg as linalg
from numpy import trace

def mvnkld (mu0, mu1, sigma0, sigma1):
    """

    Returns the Kullback-Leibler Divergence (KLD) between two normal distributions.

    """
    k = len (mu0)
    assert k == len (mu1)
    delta = mu1 - mu0
    (sign0, logdet0) = linalg.slogdet (sigma0)
    (sign1, logdet1) = linalg.slogdet (sigma1)
    lndet = logdet0 - logdet1
    A = trace (linalg.solve (sigma1, sigma0))
    B = delta.T.dot (linalg.solve (sigma1, delta))
    return 0.5 * (A + B - k - lndet)
