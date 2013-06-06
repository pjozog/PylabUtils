#!/usr/bin/env python2

from pylab import *

def rotz (h):

    c = cos (h)
    s = sin (h)

    I = ones (c.shape)
    O = zeros (c.shape)

    C_x_h = array ([[c,   s,  O],
                    [-s,   c,  O],
                    [O,  O,  I]])
    return C_x_h