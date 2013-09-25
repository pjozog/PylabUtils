import pylab as pl
import re

import scipy.sparse

def readSparseSystem (filename):
    """

    Convert's iSAM library's output (when printing sparse 
    matrices) to a scipy sparse matrix

    Returns
    -------
    
    a sparse COO matrix, the Cholesky factor R of the 
    information matrix
    
    """
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

