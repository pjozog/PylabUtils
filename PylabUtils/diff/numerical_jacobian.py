#!/usr/bin/env python2

import numpy as np

def numerical_jacobian (fhandle, x, **args):
    """

    Compute numerical Jacobian for fhandle, evaluated at x

    fhandle should accept a length-N array, and optional kwargs arguments

    Examples
    --------

    >>> f = sin
    >>> x = array([pi])
    >>> J = numerical_jacobian (f, x)

    """
    
    y = fhandle (x, **args)
    numRows, numCols = (len (y), len (x))
    J = np.zeros ((numRows, numCols))

    for col in range (0, numCols):
        xPrime = x.copy ()
        deltaX = max (1e-4*x[col], 1e-6)
        xPrime[col] += deltaX
        yPrime = fhandle (xPrime, **args)
        J[:, col] = (yPrime - y) / deltaX

    return J
