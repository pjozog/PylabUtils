from pylab import *

import dofs

def xyz (pose):
    return pose[dofs.X:dofs.Z+1]
