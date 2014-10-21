#!/usr/bin/env python2

import numpy

def rotx (r):
    """

    Comput the 3x3 rotation matrix from the roll angle, r
    
    """

    c = numpy.cos (r)
    s = numpy.sin (r)

    I = numpy.ones (c.shape)
    O = numpy.zeros (c.shape)

    C_x_r = numpy.array ([[I,   O,  O],
                          [O,   c,  s],
                          [O,  -s,  c]])
    return C_x_r
