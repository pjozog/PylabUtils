#!/usr/bin/env python

import numpy

def circularMean (samples, weights=None):
    if weights is None:
        N = len (samples)
        sinSum = 1.0/N * sum (numpy.sin (samples))
        cosSum = 1.0/N * sum (numpy.cos (samples))
    else:
        sinSum = sum (weights * numpy.sin (samples))
        cosSum = sum (weights * numpy.cos (samples))
    return numpy.arctan2 (sinSum, cosSum)
