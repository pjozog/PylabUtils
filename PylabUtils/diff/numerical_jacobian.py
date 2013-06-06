#!/usr/bin/env python2

from pylab import *

def numerical_jacobian (fhandle, x, **args):
    
    y = fhandle (x, **args)
    
    numRows, numCols = (len (y), len (x))

    J = zeros ((numRows, numCols))
    for col in range (0, numCols):
        xPrime = x.copy ()
        deltaX = max (1e-4*x[col], 1e-6)
        xPrime[col] += deltaX
        yPrime = fhandle (xPrime, **args)
        J[:, col] = (yPrime - y) / deltaX

    return J
