from pylab import *

from . import dofs

def xyzquat2matrix (xyz, quat):
    """

    Returns
    -------

    4x4 transformation matrix from 3D position (xyz) and 4D
    quaternion vector

    """
    (w, x, y, z) = (quat[0], quat[1], quat[2], quat[3])

    H = array ([[w*w + x*x - y*y - z*z,    2*x*y - 2*w*z,         2*x*z + 2*w*y,         xyz[dofs.X]],
                [2*x*y + 2*w*z,            w*w - x*x + y*y - z*z, 2*y*z - 2*w*x,         xyz[dofs.Y]],
                [2*x*z - 2*w*y,            2*y*z + 2*w*x,         w*w - x*x - y*y + z*z, xyz[dofs.Z]],
                [0,                        0,                     0,                     1]])
    return H
