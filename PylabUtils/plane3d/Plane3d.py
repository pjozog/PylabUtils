from pylab import *

from .. import dm

import ops

class Plane3d (object):

    def __init__ (self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self._computeAzimElev ()

    def _computeAzimElev (self):
        self.azim, self.elev, self.d = dm.trans2dm (self.x, self.y, self.z)

    def oplus (self, pose):
        return ops.oplus (self, pose)

    def ominus (self, pose):
        return ops.ominus (self, pose)

    def __repr__ (self):
        return 'X: %1.6f\nY: %1.6f\nZ: %1.6f\nA: %1.6f\nE: %1.6f\nD: %1.6f\n' % (self.x, self.y, self.z, self.azim, self.elev, self.d)
