from pylab import *

import dofs

def rph (pose):
    """
    
    Return the 3 Euler angles from the length-6 vector
    that describes a 6-DOF pose

    """
    return pose[dofs.ROLL:dofs.HEADING+1]
