#!/usr/bin/env python2

from pylab import *

def rotx (r):
    """

    Comput the 3x3 rotation matrix from the roll angle, r
    
    """

    c = cos (r)
    s = sin (r)

    I = ones (c.shape)
    O = zeros (c.shape)

    C_x_r = array ([[I,   O,  O],
                    [O,   c,  s],
                    [O,  -s,  c]])
    return C_x_r
