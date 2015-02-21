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

        vals = angle.copy ()
        indsPositive = numpy.logical_and (angleMask, vals >= 0)
        indsNegative = numpy.logical_and (angleMask, vals < 0)

        valsPositive = vals[indsPositive]
        valsPositive = numpy.mod (valsPositive + numpy.pi, 2*numpy.pi) - numpy.pi

        valsNegative = vals[indsNegative]
        valsNegative = numpy.mod (valsNegative - numpy.pi, -2*numpy.pi) + numpy.pi
        
        vals[indsPositive] = valsPositive
        vals[indsNegative] = valsNegative
        return vals
