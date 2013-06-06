#!/usr/bin/env python2

from pylab import *

def roty (p):

    c = cos (p)
    s = sin (p)

    I = ones (c.shape)
    O = zeros (c.shape)

    C_x_p = array ([[c,   O,  -s],
                    [O,   I,  O],
                    [s,  O,  c]])
    return C_x_p
