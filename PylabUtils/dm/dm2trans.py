from pylab import *

def dm2trans (a, e, m):
    """

    Returns
    -------
    
    xyz translation vector from azimuth, elevation, and 
    magnitude
    
    """

    tz = m*sin (e)
    tx = m*cos (e)*cos (a)
    ty = m*cos (e)*sin (a)

    return array([tx, ty, tz])
