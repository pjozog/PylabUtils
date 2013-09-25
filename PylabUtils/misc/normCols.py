from pylab import *

from normRows import normRows

def normCols (X):
    """

    Return the norms of each column of X (NxM) in a length-M array

    Examples
    --------
    
    >>> A = array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
    >>> normCols (A)
    
    """
    return normRows (X.transpose ())
