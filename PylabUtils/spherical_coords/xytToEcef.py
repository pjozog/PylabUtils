#!/usr/bin/env python

from pylab import array, cos, sin, append
from .rotecef import rotecef

from .. import coord_xfms

def xytToEcef (lat, long, height, bearing, radius):

    x = (radius + height) * cos (lat) * cos (long)
    y = (radius + height) * cos (lat) * sin (long)
    z = (radius + height) * sin (lat)

    Rtmp = rotecef (lat, long);

    R = coord_xfms.rotz (bearing).dot (Rtmp)

    rph = coord_xfms.rot2rph (R.transpose ());

    pose = array([])
    pose = append (pose, array ([x, y, z]))
    pose = append (pose, rph)

    return pose
