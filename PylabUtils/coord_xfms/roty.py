#!/usr/bin/env python2

import numpy

def roty (p):
    """

    Comput the 3x3 rotation matrix from the pitch angle, p
    
    """

    c = numpy.cos (p)
    s = numpy.sin (p)

    I = numpy.ones (c.shape)
    O = numpy.zeros (c.shape)

    C_x_p = numpy.array ([[c,   O,  -s],
                          [O,   I,  O],
                          [s,  O,  c]])
    return C_x_p
