#!/usr/bin/python

from pylab import zeros, array, cos, sin

def rotecef (lat, long):
    clat = cos (lat)
    slat = sin (lat)
    clong = cos (long)
    slong = sin (long);
    zer = zeros (clat.shape);

    R = array([[-slat*clong, -slat*slong, clat],
               [-slong, clong, zer],
               [-clat*clong, -clat*slong, -slat]])

    return R
