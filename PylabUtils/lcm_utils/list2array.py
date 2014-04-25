from pylab import *

def list2array (l, shape):
    """

    Convert a python list to a 2D numpy array

    """
    if len (shape) > 1:
        assert len (l) == prod (shape)
    else:
        assert len (l) == shape[0]
        
    return array (l).reshape (shape)
