import numpy as np

def normRows (X):
    """

    Return the norms of each row of X (NxM) in a length-N array

    Examples
    --------
    
    >>> A = array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
    >>> normRows (A)
    
    """
    return np.sum(np.abs(X)**2 ,axis=-1)**(1./2)
