import pylab as pl
import numpy as np
from .. import coord_xfms
from .. import plane3d
from . import homogeneous

class Camera:
    
    def __init__ (self, x_wc, K):
        self.x_wc = x_wc
        self.x_cw = coord_xfms.ssc.inverse (self.x_wc)

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
        uvMat = np.atleast_2d (uv)
        if uvMat.shape[0] == 1:
            uvMat = uvMat.T
        npts = uvMat.shape[1]
        invPx = self.pinvP.dot (homogeneous.homogenize (uvMat))
        XLambda = invPx + pl.tile (lam*homogeneous.homogenize (self.C), (npts, 1)).T
        return homogeneous.dehomogenize (XLambda)

    def normalize (self, uv):
        return homogeneous.dehomogenize (self.invK.dot (homogeneous.homogenize (uv)))

    # plane_c is plane expressed in camera frame
    def backprojectOnPlane (self, uv, plane_c):
        # get a point on the plane
        plane_w = plane_c.oplus (self.x_wc)
        p0 = self.x_wc[0:3] - plane_w.asArray ()
        l0 = self.x_wc[0:3]

        # these are in the camera frame, we want the world frame
        l_end_cam = self.invK.dot (homogeneous.homogenize (uv))
        l_end = homogeneous.dehomogenize (self.cHw.dot (homogeneous.homogenize (l_end_cam)))
        l_start = l0

        # subtract l_start to every column in l_end
        l = (l_end.T - l_start).T

        # use the formula from wikipedia
        n = plane_w.asArray ()
        n = n / np.linalg.norm (n)

        d = ((p0.T - l0).T.dot (n)) / (l.T.dot (n))

        # scale every column in l by the corresponding element of d
        tmp = l * d[None,:]

        # add l0 to every column in tmp (these are the intersections)
        return (tmp.T + l0).T

# taken from zhang's Camera Calibration, Chapter 1
def cameraFromProjectionMat (P):
    B = P[0:3,0:3]
    b = P[:,3]
    BBT = B.dot (B.T)
    scale = 1. / BBT[2,2]
    BBT *= scale
    cx = BBT[0,2]
    cy = BBT[1,2]
    fy = np.sqrt (BBT[1,1] - cy**2)
    gamma = (BBT[0,1] - cx*cy) / fy
    fx = np.sqrt (BBT[0,0] - cx**2 - gamma**2)

    K = np.array ([[fx, gamma, cx],[0, fy, cy],[0, 0, 1.]])
    R = np.linalg.inv (K).dot (B)
    t = np.linalg.inv (K).dot (b)

    rph = coord_xfms.rot2rph (R)
    pose_ = np.concatenate ((t, rph))
    pose = coord_xfms.ssc.inverse (pose_)

    return Camera (pose, K)
