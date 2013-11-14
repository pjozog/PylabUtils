#!/usr/bin/env python

import scipy.linalg

from numpy import zeros, real, sum, outer

def unscented_transform (mu, Sigma, alpha=1, kappa=0, beta=2):
    n = len (mu)
    lam = alpha**2 * (n+kappa) - n
    sigmaPoints = zeros (n,)
    
    U = real (scipy.linalg.sqrtm ((n+lam) * Sigma))
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

def unscented_func (f, sigmaPoints, meanWeight, covWeight, **kwargs):
    n = sigmaPoints.shape[1]

    y = f (sigmaPoints[:,0], **kwargs)
    m = len (y)

    y = zeros ((m, n))

    for i in range (n):
        y[:,i] = f (sigmaPoints[:,i], **kwargs)

    muPrime = sum (y * meanWeight, axis=1)

    SigmaPrime = zeros ((m, m))
    for i in range (n):
        SigmaPrime += covWeight[i] * outer (y[:,i] - muPrime, (y[:,i] - muPrime))

    return muPrime, SigmaPrime
