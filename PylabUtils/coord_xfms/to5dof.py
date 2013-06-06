from pylab import *

from .. import dm

from xyz import xyz
from rph import rph
import dofs

def to5dof (xij):
    aem = dm.trans2dm (xij[dofs.X], xij[dofs.Y], xij[dofs.Z])
    return concatenate ((aem[0:2], rph (xij)))
