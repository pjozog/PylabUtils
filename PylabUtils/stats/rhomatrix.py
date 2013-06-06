from pylab import *

def rhomatrix (Sigma):
    d = sqrt (diag (Sigma))
    R = Sigma / (outer (d, d))
    return R
