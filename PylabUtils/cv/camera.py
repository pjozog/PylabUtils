import pylab as pl
from .. import coord_xfms
from .. import plane3d
from . import homogeneous

class Camera:
    
    def __init__ (self, x_wc, K):
        self.x_wc = x_wc
        self.x_cw = coord_xfms.ssc_inverse (self.x_wc)

        # camera calibration matrix
        self.K = K
        
        # camera center
        self.C = self.x_wc[0:3]

        # transforms points in world frame to points in camera frame
        self.wHc = coord_xfms.xyzrph2matrix (self.x_cw)
        # transforms points in camera frame to points in world frame
        self.cHw = coord_xfms.xyzrph2matrix (self.x_wc)

        # the stupid [R t] notation that I absolutely hate
        self.Rt = self.wHc[0:3,:]
        
        # projects points in world frame to image plane of camera
        self.P = K.dot (self.Rt)

        # used for normalized image points
        self.invK = pl.inv (K[0:3,0:3])

        # used in back-projecting points to rays
        self.pinvP = pl.pinv (self.P)

    def project (self, X):
        return homogeneous.dehomogenize (self.P.dot (homogeneous.homogenize (X)))

    def transformPoints (self, X, transform=None):
        if transform is None:
            transform = self.wHc
        return homogeneous.dehomogenize (transform.dot (homogeneous.homogenize (X)))

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

    def backprojectOnPlane (self, uv, plane):
        # rotate the plane so that it's the ground plane (0, 0, 1)
        groundPlane = plane3d.Plane3d (0, 0, 1)
        RPlaneToGround = plane.rot (groundPlane)
        rph = coord_xfms.rot2rph (RPlaneToGround.T)

        # "x_cnew" : "Transformation from camera frame to new frame"
        x_cnew = pl.array ([-plane.x, -plane.y, -plane.z, rph[0], rph[1], rph[2]])
        # "x_wnew" : "Transformation from world frame to new frame"
        x_wnew = coord_xfms.ssc_head2tail (self.x_wc, x_cnew)
        # "x_newc" : "Transformation from new frame to camera frame"
        x_newc = coord_xfms.ssc_inverse (x_cnew)

        # camera in shifted reference frame
        camnew = Camera (x_newc, self.K)

        # we know if we back-projected the 2D pixel point to 3D space in this new reference frame,
        # it will have z coordinate of zero.  Therefore, discard the third column of camera
        # projection matrix P
        Preduced = camnew.P[:,[0, 1, 3]]

        # now we can recover the X Y (and Z, since it's zero) of the 3D point in rotated reference frame
        backproj = homogeneous.dehomogenize (pl.inv (Preduced).dot (homogeneous.homogenize (uv)))
        Xnew = pl.row_stack ((backproj[0], backproj[1], pl.zeros (backproj[0].shape)))

        # transform back to original reference frame
        H = coord_xfms.xyzrph2matrix (x_wnew)
        X = homogeneous.dehomogenize (H.dot (homogeneous.homogenize (Xnew)))
        return X
