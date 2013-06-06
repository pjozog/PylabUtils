#!/usr/bin/env python2

from pylab import *

def calculateEllipseXY(mu, Sigma, k2, N=20):
    
    theta = linspace (0, 2*pi, N)
    CIRCLE = array ([cos (theta), sin (theta)])

    eigs, eigvs = eig ((Sigma + Sigma.transpose())/2)

    A = eigvs.dot((diag (k2*eigs))**.5)
    
    Y = A.dot(CIRCLE)
    
    x = mu[0] + Y[0,:].transpose()
    y = mu[1] + Y[1,:].transpose()
    
    return (x, y)
