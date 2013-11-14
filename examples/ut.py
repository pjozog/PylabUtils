#!/usr/bin/env python

from pylab import *

import PylabUtils as plu

mu = 2*ones (3,)
Sigma = .2 * eye (3)

def f (x, **kwargs):
    return array ([x[0]**1, x[1]**2, x[2]**3])

sigmaPoints, meanWeight, covWeight = plu.ut.unscented_transform (mu, Sigma)

muPrime, SigmaPrime = plu.ut.unscented_func (f, sigmaPoints, meanWeight, covWeight)

print SigmaPrime

J = plu.diff.numerical_jacobian (f, mu)
print J.dot (Sigma).dot (J.T)
