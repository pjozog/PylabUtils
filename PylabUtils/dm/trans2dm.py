from pylab import *

from .. import misc

def trans2dm (x, y, z):
    """

    Returns
    -------
    
    azimuth, elevation, and magnitude translation vector from
    xyz translation
    
    """

    a = arctan2 (y, x)
    e = arctan2 (z, sqrt (x**2 + y**2))
    m = misc.normCols (array ([x, y, z]))

    return array([a, e, m])
