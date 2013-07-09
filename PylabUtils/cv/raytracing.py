#!/usr/bin/env python

import pylab as pl
from .. import coord_xfms
import homogeneous

class RayTracer:
    
    def __init__ (self, camera):
        self.camera = camera

    def trace (self, uv, lam):
        invPx = self.camera.pinvP.dot (homogeneous.homogenize (uv))
        XLambda = invPx + lam*homogeneous.homogenize (self.camera.C)
        return homogeneous.dehomogenize (XLambda)
