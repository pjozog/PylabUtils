#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from shapely.geometry import polygon
import scipy.stats

import PylabUtils as plu

set_corners = None

fig2, ax2 = plt.subplots()

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.36)

ax_std_x = plt.axes([0.25, 0.40 - 0.10, 0.65, 0.01])
ax_std_y = plt.axes([0.25, 0.40 - 0.12, 0.65, 0.01])
ax_std_z = plt.axes([0.25, 0.40 - 0.14, 0.65, 0.01])
ax_std_r = plt.axes([0.25, 0.40 - 0.16, 0.65, 0.01])
ax_std_p = plt.axes([0.25, 0.40 - 0.18, 0.65, 0.01])
ax_std_h = plt.axes([0.25, 0.40 - 0.20, 0.65, 0.01])

ax_x_gc_x = plt.axes([0.25, 0.40 - 0.22, 0.65, 0.01])
ax_x_gc_y = plt.axes([0.25, 0.40 - 0.24, 0.65, 0.01])
ax_x_gc_z = plt.axes([0.25, 0.40 - 0.26, 0.65, 0.01])
ax_x_gc_r = plt.axes([0.25, 0.40 - 0.28, 0.65, 0.01])
ax_x_gc_p = plt.axes([0.25, 0.40 - 0.30, 0.65, 0.01])
ax_x_gc_h = plt.axes([0.25, 0.40 - 0.32, 0.65, 0.01])

ax_compute = plt.axes([0.25, 0.40 - 0.38, 0.25, 0.03])
ax_re = plt.axes([0.65, 0.40 - 0.38, 0.25, 0.03])

slider_x_gc_x = Slider(ax_x_gc_x, 'x', -1.0, 1.0, 0.)
slider_x_gc_y = Slider(ax_x_gc_y, 'y', -1.0, 1.0, 0.)
slider_x_gc_z = Slider(ax_x_gc_z, 'z', 0.000, 50.0, 0.)
slider_x_gc_r = Slider(ax_x_gc_r, 'x-ax rot', -45, 45, 0.)
slider_x_gc_p = Slider(ax_x_gc_p, 'y-ax rot', -45, 45, 0.)
slider_x_gc_h = Slider(ax_x_gc_h, 'z-ax rot', -45, 45, 0.)

slider_std_x = Slider(ax_std_x, 'sigma x', 0., 1.0, 0.01)
slider_std_y = Slider(ax_std_y, 'sigma y', 0., 1.0, 0.01)
slider_std_z = Slider(ax_std_z, 'sigma z', 0., 1.0, 0.01)
slider_std_r = Slider(ax_std_r, 'sigma x-ax rot', 0., 5.0, 0.1)
slider_std_p = Slider(ax_std_p, 'sigma y-ax rot', 0., 5.0, 0.1)
slider_std_h = Slider(ax_std_h, 'sigma z-ax rot', 0., 5.0, 0.1)

button = Button(ax_compute, 'Run Monte-Carlo', hovercolor='0.975')
button_re = Button(ax_re, 'Compute Repr. Err.', hovercolor='0.975')

# pose of camera in global frame
x_gc = np.zeros(6,)

# pose of box in global frame
X_OFFSET = 0.
Y_OFFSET = 0.5
x_gbox = np.array([0., 0.5, 50., 0., 0., 0.])

# corners of box (2x2x2m cube, kinda like a sedan)
# WIDTH = 2                         # x
# HEIGHT =    2                     # y
# DEPTH = 2                         # z

# corners of lane marker box
WIDTH = 0.1                     # x
HEIGHT = 0.01                   # y
DEPTH = 3.048                   # z

corners = np.column_stack((np.array([-WIDTH*0.5, -HEIGHT*0.5, -DEPTH*0.5]),
                           np.array([-WIDTH*0.5, -HEIGHT*0.5, +DEPTH*0.5]),
                           np.array([-WIDTH*0.5, +HEIGHT*0.5, -DEPTH*0.5]),
                           np.array([-WIDTH*0.5, +HEIGHT*0.5, +DEPTH*0.5]),
                           np.array([+WIDTH*0.5, -HEIGHT*0.5, -DEPTH*0.5]),
                           np.array([+WIDTH*0.5, -HEIGHT*0.5, +DEPTH*0.5]),
                           np.array([+WIDTH*0.5, +HEIGHT*0.5, -DEPTH*0.5]),
                           np.array([+WIDTH*0.5, +HEIGHT*0.5, +DEPTH*0.5])))

CAM_WIDTH = 1936
CAM_HEIGHT = 1456
K = np.array([[1735.109, 0.00000000, 942.9755],
              [0.00000000, 1728.963, 717.8277],
              [0., 0., 1.]])

NEAR_FACE = [0,4,6,2,0]
TOP_FACE = [0,4,5,1,0]
FACE_OF_INTEREST = TOP_FACE

def overlap(x, **kwargs):
    x_gc_noisy = np.copy(kwargs['x_gc_true'])
    x_gc_noisy[0] = x[0]
    x_gc_noisy[1] = x[1]
    x_gc_noisy[2] = x[2]
    x_gc_noisy[3] = x[3]
    x_gc_noisy[4] = x[4]
    x_gc_noisy[5] = x[5]

    x_gc_true = kwargs['x_gc_true']
    K = kwargs['K']

    camera_noisy = plu.cv.Camera(x_gc_noisy, K)
    camera_true = plu.cv.Camera(x_gc_true, K)

    corners = kwargs['corners']
    corners_global = plu.cv.homogeneous.dehomogenize(plu.coord_xfms.xyzrph2matrix(x_gbox).dot(plu.cv.homogeneous.homogenize(corners)))

    corners_uv_noisy = camera_noisy.project(corners_global)
    corners_uv_true = camera_true.project(corners_global)

    region_noisy = polygon.Polygon(corners_uv_noisy[:,FACE_OF_INTEREST].T)
    region_true = polygon.Polygon(corners_uv_true[:,FACE_OF_INTEREST].T)

    common_area = region_noisy.intersection(region_true).area
    combined_area = region_noisy.union(region_true).area

    percent_overlap = 100*(1. - ((region_true.area - common_area) / region_true.area))

    return np.array([percent_overlap])

def run_monte_carlo(event):
    x_gc[0] = slider_x_gc_x.val
    x_gc[1] = slider_x_gc_y.val
    x_gc[2] = slider_x_gc_z.val
    x_gc[3] = slider_x_gc_r.val * np.pi/180
    x_gc[4] = slider_x_gc_p.val * np.pi/180
    x_gc[5] = slider_x_gc_h.val * np.pi/180
    camera = plu.cv.Camera(x_gc, K)

    Sigma = np.zeros((6,6))

    Sigma[0,0] = (slider_std_x.val)**2
    Sigma[1,1] = (slider_std_y.val)**2
    Sigma[2,2] = (slider_std_z.val)**2
    Sigma[3,3] = (slider_std_r.val * np.pi/180)**2
    Sigma[4,4] = (slider_std_p.val * np.pi/180)**2
    Sigma[5,5] = (slider_std_h.val * np.pi/180)**2

    args = {'K' : K, 'x_gc_true' : x_gc, 'corners' : corners}
    N = 3000
    samps_in = plu.stats.mvnrnd(x_gc, Sigma, N)
    samps = np.zeros(N,)
    for i in range(N):
        samp_in = samps_in[:,i]
        samps[i] = overlap(samp_in, **args)

    muPrimeMc = np.mean(samps)
    SigmaPrimeMc = np.var(samps)

    ax2.clear()

    ax2.set_xlim([0, 100.])
    ax2.set_xlabel('Percent Overlap')
    ax2.set_ylabel('Relative frequency')
    ax2.hist(samps, bins=20, normed=True)
    x = np.linspace(-10, 110, 3000)
    ax2.plot(x, scipy.stats.norm.pdf(x, muPrimeMc, np.sqrt(SigmaPrimeMc)), 'r')
    fig2.canvas.draw()

def update(val=None):
    x_gc[0] = slider_x_gc_x.val
    x_gc[1] = slider_x_gc_y.val
    x_gc[2] = slider_x_gc_z.val
    x_gc[3] = slider_x_gc_r.val * np.pi/180
    x_gc[4] = slider_x_gc_p.val * np.pi/180
    x_gc[5] = slider_x_gc_h.val * np.pi/180
    camera = plu.cv.Camera(x_gc, K)

    args = {'K' : K, 'x_gc_true' : x_gc, 'corners' : corners}

    corners_global = plu.cv.homogeneous.dehomogenize(plu.coord_xfms.xyzrph2matrix(x_gbox).dot(plu.cv.homogeneous.homogenize(corners)))

    corners_uv = camera.project(corners_global)

    ax.clear()
    ax.axis('equal')
    ax.set_ylim([-100, CAM_HEIGHT + 100])
    ax.set_xlim([-100, CAM_WIDTH + 100])
    ax.set_ylim(ax.get_ylim()[::-1])
    ax.set_ylabel('Height (pixels)')
    ax.set_xlabel('Width (pixels)')
    ax.grid('on')

    ax.plot(corners_uv[0,[0,1]], corners_uv[1,[0,1]], 'r', linewidth=3)
    ax.plot(corners_uv[0,[1,5]], corners_uv[1,[1,5]], 'r', linewidth=3)
    ax.plot(corners_uv[0,[5,4]], corners_uv[1,[5,4]], 'r', linewidth=3)
    ax.plot(corners_uv[0,[4,0]], corners_uv[1,[4,0]], 'r', linewidth=3)

    ax.plot(corners_uv[0,[0,2]], corners_uv[1,[0,2]], 'g', linewidth=3)
    ax.plot(corners_uv[0,[2,3]], corners_uv[1,[2,3]], 'g', linewidth=3)
    ax.plot(corners_uv[0,[3,1]], corners_uv[1,[3,1]], 'g', linewidth=3)

    ax.plot(corners_uv[0,[3,7]], corners_uv[1,[3,7]], 'b', linewidth=3)
    ax.plot(corners_uv[0,[7,6]], corners_uv[1,[7,6]], 'b', linewidth=3)
    ax.plot(corners_uv[0,[6,2]], corners_uv[1,[6,2]], 'b', linewidth=3)

    ax.plot(corners_uv[0,[7,5]], corners_uv[1,[7,5]], 'k', linewidth=3)
    ax.plot(corners_uv[0,[4,6]], corners_uv[1,[4,6]], 'k', linewidth=3)

    ax.plot([0, 0, CAM_WIDTH, CAM_WIDTH, 0], [0, CAM_HEIGHT, CAM_HEIGHT, 0, 0], 'k')

    if set_corners is not None:
        ax.plot(set_corners[0,:], set_corners[1,:], 'k', linewidth=3)

    fig.canvas.draw()

def update_set_corners(val=None):
    global set_corners

    x_gc[0] = slider_x_gc_x.val
    x_gc[1] = slider_x_gc_y.val
    x_gc[2] = slider_x_gc_z.val
    x_gc[3] = slider_x_gc_r.val * np.pi/180
    x_gc[4] = slider_x_gc_p.val * np.pi/180
    x_gc[5] = slider_x_gc_h.val * np.pi/180
    camera = plu.cv.Camera(x_gc, K)

    args = {'K' : K, 'x_gc_true' : x_gc, 'corners' : corners}

    corners_global = plu.cv.homogeneous.dehomogenize(plu.coord_xfms.xyzrph2matrix(x_gbox).dot(plu.cv.homogeneous.homogenize(corners)))

    corners_uv = camera.project(corners_global)
    set_corners = corners_uv[:,FACE_OF_INTEREST]

    update()

button.on_clicked(run_monte_carlo)
button_re.on_clicked(update_set_corners)

slider_x_gc_x.on_changed(update)
slider_x_gc_y.on_changed(update)
slider_x_gc_z.on_changed(update)
slider_x_gc_r.on_changed(update)
slider_x_gc_p.on_changed(update)
slider_x_gc_h.on_changed(update)

slider_std_x.on_changed(update)
slider_std_y.on_changed(update)
slider_std_z.on_changed(update)
slider_std_r.on_changed(update)
slider_std_p.on_changed(update)
slider_std_h.on_changed(update)

update()
plt.show()
