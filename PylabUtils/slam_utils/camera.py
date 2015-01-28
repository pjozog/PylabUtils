import numpy as np

from .. import dm
from .. import stats

def _f (x, **kwargs):
    xyz = dm.dm2trans (x[0], x[1], abs (x[2]))
    rph = x[3:]
    return np.concatenate ((xyz, rph))

def approx5DofAs6Dof (z, R, N=200, scaleMean=1.0, scaleVar=100):
    mu = np.array ([z[0], z[1], scaleMean, z[2], z[3], z[4]])
    Sigma = np.zeros ((6,6))
    Sigma[0:2,0:2] = stats.margcov (R, [0, 1])
    Sigma[2,2] = scaleVar
    Sigma[3:6,3:6] = stats.margcov (R, [2, 3, 4])

    inSamples = stats.mvnrnd (mu, Sigma, N)
    outSamples = _f (inSamples)
    return (np.mean (outSamples, axis=1), np.cov (outSamples))
