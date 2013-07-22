import pylab as pl
import re

import scipy.sparse

def readSparseSystem (filename):
    f = open (filename, 'r')
    line = f.readline ()
    f.close ()
    dimStr = re.search ('[0-9]+x[0-9]+', line).group (0)
    dim = int (dimStr.split ('x')[0])

    data = pl.genfromtxt (filename)
    data = data[1:,:]
    rows = data[:,0].astype (int)
    cols = data[:,1].astype (int)
    vals = data[:,2]

    R = scipy.sparse.coo_matrix ((vals, (rows, cols)), shape=(dim,dim))
    return R

