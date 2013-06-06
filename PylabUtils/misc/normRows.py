from pylab import *

def normRows (X):
    return np.sum(np.abs(X)**2 ,axis=-1)**(1./2)
