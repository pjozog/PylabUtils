#!/usr/bin/env python

def margcov (Sigma, variables):
    """

    Marginalize a covariance matrix (strike rows and columns).  variables is a list of indeces.

    Example:
    Sigma = diag ([1,2,3])
    margcov (Sigma, [1,2])      # prints diag([2,3])

    """
    
    return Sigma[variables,:][:,variables]
