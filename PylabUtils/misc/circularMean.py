#!/usr/bin/env python

import numpy

def circularMean (samples, weights=None):
    if weights is None:
        sinSum = sum (numpy.sin (samples))
        cosSum = sum (numpy.cos (samples))
    else:
        sinSum = sum (weights * numpy.sin (samples))
        cosSum = sum (weights * numpy.cos (samples))
    return numpy.arctan2 (sinSum, cosSum)
