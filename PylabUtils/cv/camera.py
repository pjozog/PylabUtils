import pylab as pl
from .. import coord_xfms
from . import homogeneous

class Camera:
    
    def __init__ (self, x_wc, K):
        self.x_wc = x_wc
        self.x_cw = coord_xfms.ssc_inverse (self.x_wc)
        
        # camera center
        self.C = self.x_wc[0:3]

        # transforms points in world frame to points in camera frame
        self.wHc = coord_xfms.xyzrph2matrix (self.x_cw)
        # transforms points in camera frame to points in world frame
        self.cHw = coord_xfms.xyzrph2matrix (self.x_wc)

        # the stupid [R t] notation that I absolutely hate
        self.Rt = self.wHc
        
        # projects points in world frame to image plane of camera
        self.P = K.dot (self.Rt)

        # used for normalized image points
        self.invK = pl.inv (K[0:3,0:3])

        # used in back-projecting points to rays
        self.pinvP = pl.pinv (self.P)

    def project (self, X):
        return homogeneous.dehomogenize (self.P.dot (homogeneous.homogenize (X)))

    # lam ("lambda") is inverse depth, in meters
    def raytrace (self, uv, lam=1):
        npts = 1
        if len (uv.shape) == 2:
            npts = uv.shape[1]
        invPx = self.pinvP.dot (homogeneous.homogenize (uv))
        if npts == 1:
            XLambda = invPx + lam*homogeneous.homogenize (self.C)
        else:
            XLambda = invPx + pl.tile (lam*homogeneous.homogenize (self.C), (npts, 1)).T
        return homogeneous.dehomogenize (XLambda)

    def normalize (self, uv):
        return homogeneous.dehomogenize (self.invK.dot (homogeneous.homogenize (uv)))
