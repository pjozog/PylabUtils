from pylab import *
import math

def mvnpdf (x, mu, Sigma):
    if not shape (x):
        normTerm = 1./sqrt (2*pi*Sigma)
        d = (x-mu)**2 * (1/Sigma)
    else:
        normTerm = (det (2*pi*Sigma))**-0.5
        d = (x-mu).dot (inv(Sigma)).dot (x-mu)
    return normTerm * exp (-0.5 * d)

def mvnlogpdf (x, mu, Sigma):
    if not shape (x):
        return log (mvnpdf (x, mu, Sigma))
    else:
        k = len (mu)
        sign, logdet = slogdet (Sigma)
        t1 = -k/2. * log (2*pi)
        t2 = -1./2 * logdet
        t3 = -1./2 * (x-mu).dot (inv (Sigma)).dot (x-mu)
        return t1 + t2 + t3
