from pylab import *

import dofs

def rph (pose):
    return pose[dofs.ROLL:dofs.HEADING+1]
