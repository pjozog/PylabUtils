import numpy as np

from .. import dm
from .. import stats

def _f (x, **kwargs):
    xyz = dm.dm2trans (x[0], x[1], abs (x[2]))
    rph = x[3:]
    return np.concatenate ((xyz, rph))

def approx5DofAs6Dof (z, R, N=200, scaleMean=0, scaleVar=1000):
    mu = np.array ([z[0], z[1], scaleMean])
    Sigma = np.zeros ((3,3))
    Sigma[0:2,0:2] = stats.margcov (R, [0, 1])
    Sigma[2,2] = scaleVar

    inSamples = stats.mvnrnd (mu, Sigma, N)
    outSamples = _f (inSamples)
    
    return (np.mean (outSamples, axis=1), np.cov (outSamples))
