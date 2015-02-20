#!/usr/bin/env python

import scipy.linalg

from numpy import zeros, real, sum, outer
from .. import misc

minimizedAngle = misc.minimizedAngle
circularMean = misc.circularMean

def unscented_transform (mu, Sigma, alpha=1, kappa=0, beta=2):
    n = len (mu)
    lam = alpha**2 * (n+kappa) - n
    sigmaPoints = zeros (n,)
    
    U = real (scipy.linalg.cholesky ((n+lam) * Sigma)).T
    meanWeight = zeros (2*n+1,)
    covWeight = zeros (2*n+1,)
    sigmaPoints = zeros ((n, 2*n+1))

    for i in range (n):
        sigmaPoints[:,i] = mu+U[:,i]
        meanWeight[i] = 1.0/(2*(n+lam))
        covWeight[i] = 1.0/(2*(n+lam))

    for i in range (n, 2*n):
        sigmaPoints[:,i] = mu-U[:,i-n]
        meanWeight[i] = 1.0/(2*(n+lam))
        covWeight[i] = 1.0/(2*(n+lam))

    meanWeight[2*n] = lam / (n+lam)
    covWeight[2*n] = lam / (n+lam) + (1 - alpha**2 + beta)
    sigmaPoints[:, 2*n] = mu

    return (sigmaPoints, meanWeight, covWeight)

def unscented_func (f, sigmaPoints, meanWeight, covWeight, angleMask=None, **kwargs):
    n = sigmaPoints.shape[1]

    y = f (sigmaPoints[:,0], **kwargs)
    m = len (y)

    y = zeros ((m, n))

    for i in range (n):
        y[:,i] = f (sigmaPoints[:,i], **kwargs)

    muPrime = sum (y * meanWeight, axis=1)
    if angleMask is not None:
        for i, mask in enumerate (angleMask):
            if mask:
                muPrime[i] = circularMean (y[i,:], weights=meanWeight)
                muPrime[i] = minimizedAngle (muPrime[i])

    SigmaPrime = zeros ((m, m))
    for i in range (n):
        if angleMask is None:
            SigmaPrime += covWeight[i] * outer (y[:,i] - muPrime, (y[:,i] - muPrime))
        else:
            SigmaPrime += covWeight[i] * outer (minimizedAngle (y[:,i] - muPrime, angleMask), 
                                                minimizedAngle (y[:,i] - muPrime, angleMask))

    return muPrime, SigmaPrime

def unscented_obs_model (f, sigmaPoints, meanWeight, covWeight, state, stateAngleMask, obsModelAngleMask, **kwargs):
    n = sigmaPoints.shape[1]
    stateLen = len (state)

    y = f (sigmaPoints[0:stateLen,0], **kwargs) + sigmaPoints[stateLen:,0]
    m = len (y)

    y = zeros ((m, n))

    for i in range (n):
        y[:,i] = f (sigmaPoints[0:stateLen,i], **kwargs) + sigmaPoints[stateLen:,i]

    muPrime = sum (y * meanWeight, axis=1)
    for i, mask in enumerate (obsModelAngleMask):
        if mask:
            muPrime[i] = circularMean (y[i,:], weights=meanWeight)
            muPrime[i] = minimizedAngle (muPrime[i])

    SigmaPrime = zeros ((m, m))
    for i in range (n):
        SigmaPrime += covWeight[i] * outer (minimizedAngle (y[:,i] - muPrime, obsModelAngleMask), 
                                            minimizedAngle (y[:,i] - muPrime, obsModelAngleMask))

    crossCov = zeros ((stateLen, m))
    for i in range (n):
        diffState = minimizedAngle (sigmaPoints[0:stateLen,i] - state, stateAngleMask)
        diffMeas = minimizedAngle (y[:,i] - muPrime, obsModelAngleMask)
        crossCov += covWeight[i] * outer (diffState, diffMeas)

    return muPrime, SigmaPrime, crossCov
