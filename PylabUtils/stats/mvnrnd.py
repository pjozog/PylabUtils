import numpy.random

def mvnrnd (mu, Sigma, N):
    """

    Draws a sample for a multi-variate Guassian with provided mean (mu) and covariance (Sigma)

    """
    ret = numpy.random.multivariate_normal (mu, Sigma, (N,)).T
    if ret.shape[1] == 1:
        return ret.reshape (ret.shape[0],)
    return ret
