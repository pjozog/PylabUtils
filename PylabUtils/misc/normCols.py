from pylab import *

from normRows import normRows

def normCols (X):
    return normRows (X.transpose ())
