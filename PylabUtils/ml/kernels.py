#!/usr/bin/env python

from numpy import exp, array, log
import numpy.linalg

def gaussProcess (x1, x2, theta):
    diff = x1 - x2
    return theta[0]*exp (-theta[1]/2 * (diff.dot (diff))) + theta[2] + theta[3]*x1.dot (x2)

def thinPlate2D (x1, x2, R):
    r = numpy.linalg.norm (x1 - x2)
    if r == 0:
        ret = R**2
    else:
        ret = 2*r**2*log (r) - (1+2*log (R))*r**2 + R**2
    return ret

def thingPlate3D (x1, x2, R):
    raise NotImplementedError ("3D Gaussian Process implicit surface kernel not implemented")
