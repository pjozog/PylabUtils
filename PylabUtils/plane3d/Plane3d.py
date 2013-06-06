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
        return 'x=%1.2f y=%1.2f z=%1.2f a=%1.2f e=%1.2f d=%1.2f' % (self.x, self.y, self.z, self.azim, self.elev, self.d)
