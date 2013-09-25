from pylab import *

from .. import dm

from xyz import xyz
from rph import rph
import dofs

def to5dof (xij):
    """

    Convert a 6-DOF pose xij to a 5-DOF measurement, like 
    what is procuced by a 2-view 3D reconstruction

    """

    aem = dm.trans2dm (xij[dofs.X], xij[dofs.Y], xij[dofs.Z])
    return concatenate ((aem[0:2], rph (xij)))
