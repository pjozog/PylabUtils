#!/usr/bin/env python2

import numpy

def rotz (h):
    """

    Comput the 3x3 rotation matrix from the heading angle, h
    
    """

    c = numpy.cos (h)
    s = numpy.sin (h)

    I = numpy.ones (c.shape)
    O = numpy.zeros (c.shape)

    C_x_h = numpy.array ([[c,   s,  O],
                          [-s,   c,  O],
                          [O,  O,  I]])
    return C_x_h
