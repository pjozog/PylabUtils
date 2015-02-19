#!/usr/bin/env python

import numpy

def minimizedAngle (angle, angleMask=None):
    if angleMask is None:
        if angle >= 0.:
            return numpy.mod (angle + numpy.pi, 2*numpy.pi) - numpy.pi
        else:
            return numpy.mod (angle - numpy.pi, -2*numpy.pi) + numpy.pi
    else:
        assert (angle.shape == angleMask.shape)
        angle2 = angle.copy ()
        for i, mask in enumerate (angleMask):
            if mask:
                angle2[i] = minimizedAngle (angle[i], None)
            else:
                angle2[i] = angle[i]
        return angle2
