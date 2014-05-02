from pylab import *

from .. import coord_xfms

import Plane3d

def rot (plane1, plane2):
    """ returns the rotation matrix that rotates plane1 to plane2"""
    axis, angle = coord_xfms.axisang (plane1.asArray (), plane2.asArray ())
    return coord_xfms.axisang2rot (axis, angle)

def ominus (plane, pose):
    """ given a vehicle pose and plane (both in global frame), compute the plane in
    vehicle's frame """

    planeXyz = plane.asArray ()
    d = norm (planeXyz)
    planeXyzUnit = planeXyz / d
    R = coord_xfms.rotxyz (pose[coord_xfms.dofs.ROLL], pose[coord_xfms.dofs.PITCH], pose[coord_xfms.dofs.HEADING])
    R = R.transpose ()
    t = pose[coord_xfms.dofs.X:coord_xfms.dofs.ROLL]

    nPoseFrame = R.dot (planeXyzUnit)
    dPoseFrame = planeXyzUnit.dot (t) + d
    nPoseFrame *= dPoseFrame
    outPlane = Plane3d.Plane3d (nPoseFrame[0], nPoseFrame[1], nPoseFrame[2])

    return outPlane

def oplus (plane, pose):
    """ given a global vehicle pose and local plane measurement in that vehicle's frame,
    predict the plane the global frame """

    poseInv = coord_xfms.ssc_inverse (pose)
    return ominus (plane, poseInv)
