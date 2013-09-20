#!/usr/bin/env python

import pylab as pl
from .. import coord_xfms
import homogeneous

class RayTracer:
    
    def __init__ (self, camera):
        self.camera = camera

    def trace (self, uv, lam):
        npts = 1
        if len (uv.shape) == 2:
            npts = uv.shape[1]
        invPx = self.camera.pinvP.dot (homogeneous.homogenize (uv))
        if npts == 1:
            XLambda = invPx + lam*homogeneous.homogenize (self.camera.C)
        else:
            XLambda = invPx + pl.tile (lam*homogeneous.homogenize (self.camera.C), (npts, 1)).T
        return homogeneous.dehomogenize (XLambda)
