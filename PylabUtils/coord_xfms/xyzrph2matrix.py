from rph2quat import rph2quat
from xyzquat2matrix import xyzquat2matrix
import dofs

def xyzrph2matrix (x):
    """
    
    Returns
    -------
    4x4 transformation matrix from x, a 6-DOF pose array

    """
    return xyzquat2matrix (x[dofs.X:dofs.ROLL], rph2quat (x[dofs.ROLL:dofs.HEADING+1]))
