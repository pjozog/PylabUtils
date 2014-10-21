import numpy as np

def dm2trans (a, e, m):
    """

    Returns
    -------
    
    xyz translation vector from azimuth, elevation, and 
    magnitude
    
    """

    tz = m*np.sin (e)
    tx = m*np.cos (e)*np.cos (a)
    ty = m*np.cos (e)*np.sin (a)

    return np.array([tx, ty, tz])
