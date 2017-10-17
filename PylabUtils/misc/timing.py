#!/usr/bin/env python

import time
from .expecting import expecting

TICKS_PER_SECOND = 1e6

def timestamp_now ():
    return time.time () * TICKS_PER_SECOND

class Timer ():
    """

    Simple timer class

    Examples
    --------

    >>> t = Timer ()
    >>> time.sleep (0.5)
    >>> print t
    >>> print t.get ()

    """
    def __init__(self):
        self.reset ()

    def reset (self):
        self._startTime = timestamp_now ()

    def get (self):
        return (timestamp_now () - self._startTime)/TICKS_PER_SECOND

    def __repr__ (self):
        return '%.3f' % (self.get ())

_global_timer = Timer ()

def tic ():
    """

    Set the start time for the global timer
    (warning: this function is not thread-safe)

    Examples
    --------

    >>> tic ()
    >>> time.sleep (0.5)
    >>> toc ()

    """
    _global_timer.reset ()

def toc ():
    """

    Stop the global timer
    (warning: this function is not thread-safe)

    Examples
    --------

    >>> tic ()
    >>> time.sleep (0.5)
    >>> toc ()

    Returns
    -------
    For one output argument, return the ellapsed time as a float
    Else, print the ellapsed time as a string and don't return anything

    """
    outputCount = expecting ()
    if outputCount == 1:
        return _global_timer.get ()
    else:
        print('Elapsed time is %f seconds.' % _global_timer.get ())
