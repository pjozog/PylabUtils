import numpy as np

def array2list (array):
    """

    Convert a matrix (2D array) to a 1D array for publishing the matrix over lcm

    """
    return np.array.reshape (-1,).tolist ()
