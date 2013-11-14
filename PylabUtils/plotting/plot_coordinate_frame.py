from pylab import *
from mpl_toolkits.mplot3d import Axes3D

from .. import coord_xfms

def plot_coordinate_frame_from_pose (x_gi, **kwargs):
    R = coord_xfms.rotxyz (x_gi[coord_xfms.dofs.ROLL], x_gi[coord_xfms.dofs.PITCH], x_gi[coord_xfms.dofs.HEADING])
    t = x_gi[0:3]
    plot_coordinate_frame (R, t, **kwargs)

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

def mayavi_plot_coordinate_frame (R, t, **kwargs):
    import mayavi.mlab

    if 'scale' not in kwargs:
        scale = 1.
    else:
        scale = kwargs['scale']

    Aref = column_stack ([scale*eye (3), zeros (3,)])
    A = column_stack ([R, t]).dot (row_stack ([Aref, ones (4,)]))

    o = A[:,3]
    i = A[:,0] - o
    k = A[:,1] - o
    l = A[:,2] - o

    if 'color' not in kwargs:
        color = 'rgb'
    else:
        color = kwargs['color']

    colorI = matplotlib.colors.ColorConverter.colors[color[0]]
    colorK = matplotlib.colors.ColorConverter.colors[color[1]]
    colorL = matplotlib.colors.ColorConverter.colors[color[2]]
    mayavi.mlab.quiver3d (o[0], o[1], o[2], i[0], i[1], i[2], color=colorI)
    mayavi.mlab.quiver3d (o[0], o[1], o[2], k[0], k[1], k[2], color=colorK)
    mayavi.mlab.quiver3d (o[0], o[1], o[2], l[0], l[1], l[2], color=colorL)

    if 'label' not in kwargs:
        label = ''
    else:
        label = kwargs['label']

    if label:
        scale = .3
        mayavi.mlab.text3d (i[0]+o[0], i[1]+o[1], i[2]+o[2], '%s (x)' % label, scale=scale)
        mayavi.mlab.text3d (k[0]+o[0], k[1]+o[1], k[2]+o[2], '%s (y)' % label, scale=scale)
        mayavi.mlab.text3d (l[0]+o[0], l[1]+o[1], l[2]+o[2], '%s (z)' % label, scale=scale)
