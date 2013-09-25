from pylab import *

import dofs

def xyz (pose):
    """
    
    Return the 3 Cartesian position from the length-6 vector
    that describes a 6-DOF pose

    """

    return pose[dofs.X:dofs.Z+1]
