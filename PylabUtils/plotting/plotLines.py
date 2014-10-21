#!/usr/bin/env python

from pylab import *

def plotLines (xpairs, ypairs, format, **args):
    """
    Plot a bunch of line segments
    """
    xlist = []
    ylist = []
    for xends,yends in zip(xpairs,ypairs):
        xlist.extend(xends)
        xlist.append(None)
        ylist.extend(yends)
        ylist.append(None)

    if xlist:
        plot (xlist, ylist, format, **args)
