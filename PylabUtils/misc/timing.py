#!/usr/bin/env python

import time
from expecting import expecting

TICKS_PER_SECOND = 1e6

def timestamp_now ():
    return time.time () * TICKS_PER_SECOND

class Timer ():
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
    _global_timer.reset ()

def toc ():
    outputCount = expecting ()
    if outputCount == 1:
        return _global_timer.get ()
    else:
        print 'Elapsed time is %f seconds.' % _global_timer.get ()
