#!/usr/bin/env python

# use with EECS 545 homework datasets

import sys, os
import numpy
from pylab import *
import PylabUtils as plu

SIGMAS = [1.0, 0.2, 10, 2]
BETAINVS = [0.1, 0.5, 0.01, 0.03]

for sigma, betaInv in zip (SIGMAS, BETAINVS):
    xFile = sys.argv[1]
    tFile = sys.argv[2]

    x = array ([numpy.loadtxt (xFile)])
    t = numpy.loadtxt (tFile)

    if len (x.shape) == 1:
        numFeats = 1
    else:
        numFeats = x.shape[0]
    numLabels = len (t)

    gp = plu.ml.GaussianProcessRegressionDense (plu.ml.kernels.sqExp, sigma,
                                                ones (numLabels,)*betaInv,
                                                x, t)
    gp.train ()
    xTest = array ([linspace (min (x[0,:]), max (x[0,:]), 100)])
    tTest = gp.predictAt (xTest)
    tSigmaTest = gp.sigmaAt (xTest, ones (numLabels,)*betaInv)

    figure ()
    plot (xTest.T, tTest)
    hold ('on')
    plot (x.T, t, 'k.')
    plusSigma = tTest + tSigmaTest
    minusSigma = tTest - tSigmaTest
    fill_between(xTest.reshape (numLabels,), plusSigma, minusSigma, color='m',alpha=.5)

    grid ('on')
    draw ()

    show ()
