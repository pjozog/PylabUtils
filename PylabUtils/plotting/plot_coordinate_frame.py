from pylab import *
from mpl_toolkits.mplot3d import Axes3D

def plot_coordinate_frame (R, t, **kwargs):
    if 'scale' not in kwargs:
        scale = 1.
    else:
        scale = kwargs['scale']
    if 'axis' not in kwargs:
        fig = figure ()
        ax = fig.add_subplot (111, projection='3d')
    else:
        ax = kwargs['axis']

    Aref = column_stack ([scale*eye (3), zeros (3,)])
    A = column_stack ([R, t]).dot (row_stack ([Aref, ones (4,)]))

    i = A[:,0]
    k = A[:,1]
    l = A[:,2]
    o = A[:,3]

    if 'color' not in kwargs:
        color = 'rgb'
    else:
        color = kwargs['color']
    ax.plot ([o[0], i[0]], [o[1], i[1]], [o[2], i[2]], color=color[0])
    ax.plot ([o[0], k[0]], [o[1], k[1]], [o[2], k[2]], color=color[1])
    ax.plot ([o[0], l[0]], [o[1], l[1]], [o[2], l[2]], color=color[2])

    if 'label' not in kwargs:
        label = ''
    else:
        label = kwargs['label']

    if label:
        ax.text (i[0], i[1], i[2], '$\mathrm{X}_%s$' % label)
        ax.text (k[0], k[1], k[2], '$\mathrm{Y}_%s$' % label)
        ax.text (l[0], l[1], l[2], '$\mathrm{Z}_%s$' % label)
