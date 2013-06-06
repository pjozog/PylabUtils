#!/usr/bin/python

from pylab import sin, cos, arctan2, sqrt, mod

def haversine (latlong1, latlong2, r):

    deltaLatlong = latlong1 - latlong2
    
    dLat = deltaLatlong[0]
    dLon = deltaLatlong[1]

    lat1 = latlong1[0]
    lat2 = latlong2[0]

    a = (sin (dLat/2) * sin (dLat/2) +
         sin (dLon/2) * sin (dLon/2) * cos (lat1) * cos (lat2))
    c = 2 * arctan2 (sqrt (a), sqrt (1-a))
    d = r * c

    # initial bearing
    y = sin (dLon) * cos (lat2)
    x = (cos (lat1)*sin (lat2) -
         sin (lat1)*cos (lat2)*cos (dLon))
    b1 = arctan2 (y, x);

    # final bearing
    dLon = -dLon
    dLat = -dLat
    tmp = lat1
    lat1 = lat2
    lat2 = tmp
    y = sin (dLon) * cos (lat2)
    x = (cos (lat1) * sin (lat2) - 
         sin (lat1) * cos (lat2) * cos (dLon))
    b2 = arctan2 (y, x)
    b2 = mod ((b2 + pi), 2*pi)

    return (d, b1, b2)
