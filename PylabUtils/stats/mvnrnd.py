#!/usr/bin/env python

from pylab import *
import numpy.random

from .. import misc

def mvnrnd (mu, Sigma, N):

    ret = numpy.random.multivariate_normal (mu, Sigma, (N,)).T
    if ret.shape[1] == 1:
        return ret.reshape (ret.shape[0],)
    return ret
