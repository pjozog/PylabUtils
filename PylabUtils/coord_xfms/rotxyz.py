#!/usr/bin/env python2

from pylab import *

def rotxyz (r, p, h):

    cr = cos(r); sr = sin(r);
    cp = cos(p); sp = sin(p);
    ch = cos(h); sh = sin(h);

    R = array([[ ch*cp,   (-sh*cr + ch*sp*sr),   ( sh*sr + ch*sp*cr)],
               [ sh*cp,   ( ch*cr + sh*sp*sr),   (-ch*sr + sh*sp*cr)],
               [-sp,          cp*sr,                  cp*cr        ]])
    return R