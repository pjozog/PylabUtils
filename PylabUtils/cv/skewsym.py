#!/usr/bin/env python

from numpy import array

def skewsym (x):
    return array ([[0, -x[2], x[1]],
                   [x[2], 0, -x[0]],
                   [-x[1], x[0], 0]])
