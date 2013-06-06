#!/usr/bin/env python2

from pylab import array, arctan2, cos, sin

def rot2rph (R):

    h = arctan2 (R[1,0], R[0,0])

    ch = cos (h)
    sh = sin (h)

    p = arctan2 (-R[2,0], R[0,0]*ch + R[1,0]*sh)

    r = arctan2 (R[0,2]*sh - R[1,2]*ch, -R[0,1]*sh + R[1,1]*ch);

    return array ([r,p,h])
