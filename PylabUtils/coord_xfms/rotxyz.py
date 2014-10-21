#!/usr/bin/env python2

import numpy as np

def rotxyz (r, p, h):
    """

    Compute the 3x3 rotation matrix R from roll, pitch, and heading Euler angles

    """

    cr = np.cos(r); sr = np.sin(r);
    cp = np.cos(p); sp = np.sin(p);
    ch = np.cos(h); sh = np.sin(h);

    R = np.array([[ ch*cp,   (-sh*cr + ch*sp*sr),   ( sh*sr + ch*sp*cr)],
                  [ sh*cp,   ( ch*cr + sh*sp*sr),   (-ch*sr + sh*sp*cr)],
                  [-sp,          cp*sr,                  cp*cr        ]])
    return R
