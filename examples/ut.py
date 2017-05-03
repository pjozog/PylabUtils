#!/usr/bin/env python

from pylab import *

import PylabUtils as plu

mu = 2*ones (3,)
Sigma = .2 * eye (3)

def f (x, **kwargs):
    return array ([x[0]**1, x[1]**2, x[2]**3, arctan2(x[2], x[1])])

sigmaPoints, meanWeight, covWeight = plu.ut.unscented_transform (mu, Sigma)

muPrime, SigmaPrime = plu.ut.unscented_func (f, sigmaPoints, meanWeight, covWeight, angleMask=np.array([False, False, True, True]))

print muPrime
print 'Unscented transform covariance estimate: '
print SigmaPrime

J = plu.diff.numerical_jacobian (f, mu)
print 'First-order covariance estimate: '
print J.dot (Sigma).dot (J.T)

# test a UKF-like observation model

# XAug is the state vector.  Contains current belief of state (x, y, theta) and bearing
# noise's mean (should be zero). Hence it's length-4
XAug = np.array ([199.6808, 278.4578, -3.0877, 0])
# covariance of XAug
SigmaAug = np.array ([[56.7689,   -0.8136,   -0.0360,         0],
                      [-0.8136,   62.3622,   -0.2751,         0],
                      [-0.0360,   -0.2751,    0.0049,         0],
                      [0,         0,         0,    0.1218]])
sigmaPoints, meanWeight, covWeight = plu.ut.unscented_transform (XAug, SigmaAug)

# predict bearing-only measurement
def observation (state, **kwargs):
    dx = kwargs['xCoord'] - state[0]
    dy = kwargs['yCoord'] - state[1]
    dist = sqrt (dx**2 + dy**2)
    obs = np.arctan2 (dy, dx) - state[2]
    return obs

stateAngleMask = np.array ([False, False, True])
obsModelAngleMask = np.array ([True])
args = {'xCoord': 21, 'yCoord': 292}
predObs, predObsCov, crossCov = plu.ut.unscented_obs_model (observation, sigmaPoints, meanWeight, covWeight,
                                                            XAug[0:3], stateAngleMask, obsModelAngleMask,
                                                            **args)

if np.allclose (predObs, np.array ([-0.1295]), atol=1e-4):
    print 'predObs checks out'
else:
    print 'ERROR: predObs is incorrect'
    sys.exit (1)

if np.allclose (predObsCov, np.array ([[0.1317]]), atol=1e-4):
    print 'predObsCov checks out'
else:
    print 'ERROR: predObsCov is incorrect'
    sys.exit (1)

if np.allclose (crossCov, np.array ([[0.0556], [0.6209], [-0.0064]]), atol=1e-4):
    print 'crossCov checks out'
else:
    print 'ERROR: crossCov is incorrect'
    sys.exit (1)

# from the EECS 568 matlab assignment:
# predictedObs =

#    -0.1295


# predictedObsCov =

#     0.1317


# crossCov =

#     0.0556
#     0.6209
#    -0.0064
