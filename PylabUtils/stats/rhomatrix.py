from pylab import *

def rhomatrix (Sigma):
    """
    
    Computes a matrix of correlation coefficients given a covariance matrix (Sigma)
    
    """
    d = sqrt (diag (Sigma))
    R = Sigma / (outer (d, d))
    return R
