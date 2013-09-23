#!/usr/bin/env python

import PylabUtils as plu
from time import sleep

SLEEP_TIME = 0.5

# no outputs
plu.misc.tic ()
sleep (SLEEP_TIME)
plu.misc.toc ()

# capture output
plu.misc.tic ()
sleep (SLEEP_TIME)
t = plu.misc.toc ()
print 'You sleeped for %f seconds!' % (t)
