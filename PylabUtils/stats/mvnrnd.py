#!/usr/bin/env python

from pylab import *

from .. import misc

def mvnrnd (mu, Sigma, N):
    
    shape = mu.shape
    x = randn (shape[0], N)
    
    sqrtSigma = cholesky (Sigma)
    
    y = sqrtSigma.dot(x)

    # this is ugly but I'm not sure how to handle the case if N is 1
    if ret.shape[1] == 1:
        return ret.reshape ((shape[0],))
    else:
        return ret
