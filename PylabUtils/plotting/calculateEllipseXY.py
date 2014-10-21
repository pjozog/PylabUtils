#!/usr/bin/env python2

from pylab import *

def calculateEllipseXY(mu, Sigma, k2, N=20):
    """

    Computes x and y values given a covariance matrix and chi-squared threshold.

    mu: length-2 mean vector
    Sigma: 2x2 covariance matrix
    k2: chi-squared threshold
    N: number of points to compute

    Example:
    mu = zeros (2,)
    Sigma = diag([1,2])
    k2 = scipy.stats.chi2.ppf (.999, 2)
    x, y = calculateEllipseXY (mu, Sigma, k2)

    """
    
    theta = linspace (0, 2*pi, N)
    CIRCLE = array ([cos (theta), sin (theta)])

    eigs, eigvs = eig ((Sigma + Sigma.transpose())/2)

    A = eigvs.dot((diag (k2*eigs))**.5)
    
    Y = A.dot(CIRCLE)
    
    x = mu[0] + Y[0,:].transpose()
    y = mu[1] + Y[1,:].transpose()
    
    return (x, y)
