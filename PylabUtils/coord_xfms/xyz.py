from pylab import *

import dofs

def xyz (pose):
    return pose[dofs.X:dofs.Y+1]
