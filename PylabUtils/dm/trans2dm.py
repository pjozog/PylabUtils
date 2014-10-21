from .. import misc

import numpy as np

def trans2dm (x, y, z):
    """

    Returns
    -------
    
    azimuth, elevation, and magnitude translation vector from
    xyz translation
    
    """

    a = np.arctan2 (y, x)
    e = np.arctan2 (z, np.sqrt (x**2 + y**2))
    m = misc.normCols (np.array ([x, y, z]))

    return np.array([a, e, m])
