#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from shapely.geometry import polygon
import scipy.stats

import PylabUtils as plu

# corners of box (2x2x2m cube, kinda like a sedan)
# WIDTH = 2                         # x
# HEIGHT =    2                     # y
# DEPTH = 2                         # z

# corners of lane marker box
WIDTH = 0.10                    # x
HEIGHT = 0.01                   # y
DEPTH = 3.048                   # z

NEAR_FACE = [0,4,6,2,0]
TOP_FACE = [0,4,5,1,0]

class Self:
    def __init__(self, width, height, depth, face_indeces):
        self.set_corners = None

        self.fig2, self.ax2 = plt.subplots()

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.36)

        self.ax_std_x = plt.axes([0.25, 0.40 - 0.10, 0.65, 0.01])
        self.ax_std_y = plt.axes([0.25, 0.40 - 0.12, 0.65, 0.01])
        self.ax_std_z = plt.axes([0.25, 0.40 - 0.14, 0.65, 0.01])
        self.ax_std_r = plt.axes([0.25, 0.40 - 0.16, 0.65, 0.01])
        self.ax_std_p = plt.axes([0.25, 0.40 - 0.18, 0.65, 0.01])
        self.ax_std_h = plt.axes([0.25, 0.40 - 0.20, 0.65, 0.01])

        self.ax_x_gc_x = plt.axes([0.25, 0.40 - 0.22, 0.65, 0.01])
        self.ax_x_gc_y = plt.axes([0.25, 0.40 - 0.24, 0.65, 0.01])
        self.ax_x_gc_z = plt.axes([0.25, 0.40 - 0.26, 0.65, 0.01])
        self.ax_x_gc_r = plt.axes([0.25, 0.40 - 0.28, 0.65, 0.01])
        self.ax_x_gc_p = plt.axes([0.25, 0.40 - 0.30, 0.65, 0.01])
        self.ax_x_gc_h = plt.axes([0.25, 0.40 - 0.32, 0.65, 0.01])

        self.ax_compute = plt.axes([0.25, 0.40 - 0.38, 0.25, 0.03])
        self.ax_re = plt.axes([0.65, 0.40 - 0.38, 0.25, 0.03])

        self.slider_x_gc_x = Slider(self.ax_x_gc_x, 'x', -1.0, 1.0, 0.)
        self.slider_x_gc_y = Slider(self.ax_x_gc_y, 'y', -1.0, 1.0, 0.)
        self.slider_x_gc_z = Slider(self.ax_x_gc_z, 'z', 0.000, 50.0, 0.)
        self.slider_x_gc_r = Slider(self.ax_x_gc_r, 'x-ax rot', -45, 45, 0.)
        self.slider_x_gc_p = Slider(self.ax_x_gc_p, 'y-ax rot', -45, 45, 0.)
        self.slider_x_gc_h = Slider(self.ax_x_gc_h, 'z-ax rot', -45, 45, 0.)

        self.slider_std_x = Slider(self.ax_std_x, 'sigma x', 0., 1.0, 0.01)
        self.slider_std_y = Slider(self.ax_std_y, 'sigma y', 0., 1.0, 0.01)
        self.slider_std_z = Slider(self.ax_std_z, 'sigma z', 0., 1.0, 0.01)
        self.slider_std_r = Slider(self.ax_std_r, 'sigma x-ax rot', 0., 5.0, 0.1)
        self.slider_std_p = Slider(self.ax_std_p, 'sigma y-ax rot', 0., 5.0, 0.1)
        self.slider_std_h = Slider(self.ax_std_h, 'sigma z-ax rot', 0., 5.0, 0.1)

        self.button = Button(self.ax_compute, 'Run Monte-Carlo', hovercolor='0.975')
        self.button_re = Button(self.ax_re, 'Compute Repr. Err.', hovercolor='0.975')

        # pose of camera in global frame
        self.x_gc = np.zeros(6,)

        # pose of box in global frame
        self.X_OFFSET = 0.
        self.Y_OFFSET = 0.5
        self.x_gbox = np.array([0., 0.5, 50., 0., 0., 0.])

        self.corners = np.column_stack((np.array([-WIDTH*0.5, -HEIGHT*0.5, -DEPTH*0.5]),
                                        np.array([-WIDTH*0.5, -HEIGHT*0.5, +DEPTH*0.5]),
                                        np.array([-WIDTH*0.5, +HEIGHT*0.5, -DEPTH*0.5]),
                                        np.array([-WIDTH*0.5, +HEIGHT*0.5, +DEPTH*0.5]),
                                        np.array([+WIDTH*0.5, -HEIGHT*0.5, -DEPTH*0.5]),
                                        np.array([+WIDTH*0.5, -HEIGHT*0.5, +DEPTH*0.5]),
                                        np.array([+WIDTH*0.5, +HEIGHT*0.5, -DEPTH*0.5]),
                                        np.array([+WIDTH*0.5, +HEIGHT*0.5, +DEPTH*0.5])))

        self.CAM_WIDTH = 1936
        self.CAM_HEIGHT = 1456
        self.K = np.array([[1735.109, 0.00000000, 942.9755],
                           [0.00000000, 1728.963, 717.8277],
                           [0., 0., 1.]])

        self.face_of_interest = face_indeces

    def overlap(self, x, **kwargs):
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
        corners_global = plu.cv.homogeneous.dehomogenize(plu.coord_xfms.xyzrph2matrix(self.x_gbox).dot(plu.cv.homogeneous.homogenize(self.corners)))

        corners_uv_noisy = camera_noisy.project(corners_global)
        corners_uv_true = camera_true.project(corners_global)

        region_noisy = polygon.Polygon(corners_uv_noisy[:,self.face_of_interest].T)
        region_true = polygon.Polygon(corners_uv_true[:,self.face_of_interest].T)

        common_area = region_noisy.intersection(region_true).area
        combined_area = region_noisy.union(region_true).area

        percent_overlap = 100*(1. - ((region_true.area - common_area) / region_true.area))

        return np.array([percent_overlap])

    def run_monte_carlo(self, event):
        self.x_gc[0] = self.slider_x_gc_x.val
        self.x_gc[1] = self.slider_x_gc_y.val
        self.x_gc[2] = self.slider_x_gc_z.val
        self.x_gc[3] = self.slider_x_gc_r.val * np.pi/180
        self.x_gc[4] = self.slider_x_gc_p.val * np.pi/180
        self.x_gc[5] = self.slider_x_gc_h.val * np.pi/180
        camera = plu.cv.Camera(self.x_gc, self.K)

        Sigma = np.zeros((6,6))

        Sigma[0,0] = (self.slider_std_x.val)**2
        Sigma[1,1] = (self.slider_std_y.val)**2
        Sigma[2,2] = (self.slider_std_z.val)**2
        Sigma[3,3] = (self.slider_std_r.val * np.pi/180)**2
        Sigma[4,4] = (self.slider_std_p.val * np.pi/180)**2
        Sigma[5,5] = (self.slider_std_h.val * np.pi/180)**2

        args = {'K' : self.K, 'x_gc_true' : self.x_gc, 'corners' : self.corners}
        N = 3000
        samps_in = plu.stats.mvnrnd(self.x_gc, Sigma, N)
        samps = np.zeros(N,)
        for i in range(N):
            samp_in = samps_in[:,i]
            samps[i] = self.overlap(samp_in, **args)

        muPrimeMc = np.mean(samps)
        SigmaPrimeMc = np.var(samps)

        self.ax2.clear()

        self.ax2.set_xlim([0, 100.])
        self.ax2.set_xlabel('Percent Overlap')
        self.ax2.set_ylabel('Relative frequency')
        self.ax2.hist(samps, bins=20, normed=True)
        x = np.linspace(-10, 110, 3000)
        self.ax2.plot(x, scipy.stats.norm.pdf(x, muPrimeMc, np.sqrt(SigmaPrimeMc)), 'r')
        self.fig2.canvas.draw()

    def update(self, val=None):
        self.x_gc[0] = self.slider_x_gc_x.val
        self.x_gc[1] = self.slider_x_gc_y.val
        self.x_gc[2] = self.slider_x_gc_z.val
        self.x_gc[3] = self.slider_x_gc_r.val * np.pi/180
        self.x_gc[4] = self.slider_x_gc_p.val * np.pi/180
        self.x_gc[5] = self.slider_x_gc_h.val * np.pi/180
        camera = plu.cv.Camera(self.x_gc, self.K)

        args = {'K' : self.K, 'x_gc_true' : self.x_gc, 'corners' : self.corners}

        corners_global = plu.cv.homogeneous.dehomogenize(plu.coord_xfms.xyzrph2matrix(self.x_gbox).dot(plu.cv.homogeneous.homogenize(self.corners)))

        corners_uv = camera.project(corners_global)

        self.ax.clear()
        self.ax.axis('equal')
        self.ax.set_ylim([-100, self.CAM_HEIGHT + 100])
        self.ax.set_xlim([-100, self.CAM_WIDTH + 100])
        self.ax.set_ylim(self.ax.get_ylim()[::-1])
        self.ax.set_ylabel('Height (pixels)')
        self.ax.set_xlabel('Width (pixels)')
        self.ax.grid('on')

        self.ax.plot(corners_uv[0,[0,1]], corners_uv[1,[0,1]], 'r', linewidth=3)
        self.ax.plot(corners_uv[0,[1,5]], corners_uv[1,[1,5]], 'r', linewidth=3)
        self.ax.plot(corners_uv[0,[5,4]], corners_uv[1,[5,4]], 'r', linewidth=3)
        self.ax.plot(corners_uv[0,[4,0]], corners_uv[1,[4,0]], 'r', linewidth=3)

        self.ax.plot(corners_uv[0,[0,2]], corners_uv[1,[0,2]], 'g', linewidth=3)
        self.ax.plot(corners_uv[0,[2,3]], corners_uv[1,[2,3]], 'g', linewidth=3)
        self.ax.plot(corners_uv[0,[3,1]], corners_uv[1,[3,1]], 'g', linewidth=3)

        self.ax.plot(corners_uv[0,[3,7]], corners_uv[1,[3,7]], 'b', linewidth=3)
        self.ax.plot(corners_uv[0,[7,6]], corners_uv[1,[7,6]], 'b', linewidth=3)
        self.ax.plot(corners_uv[0,[6,2]], corners_uv[1,[6,2]], 'b', linewidth=3)

        self.ax.plot(corners_uv[0,[7,5]], corners_uv[1,[7,5]], 'k', linewidth=3)
        self.ax.plot(corners_uv[0,[4,6]], corners_uv[1,[4,6]], 'k', linewidth=3)

        self.ax.plot([0, 0, self.CAM_WIDTH, self.CAM_WIDTH, 0], [0, self.CAM_HEIGHT, self.CAM_HEIGHT, 0, 0], 'k')

        if self.set_corners is not None:
            self.ax.plot(self.set_corners[0,:], self.set_corners[1,:], 'k', linewidth=3)

        self.fig.canvas.draw()

    def update_set_corners(self, val=None):
        global set_corners

        self.x_gc[0] = self.slider_x_gc_x.val
        self.x_gc[1] = self.slider_x_gc_y.val
        self.x_gc[2] = self.slider_x_gc_z.val
        self.x_gc[3] = self.slider_x_gc_r.val * np.pi/180
        self.x_gc[4] = self.slider_x_gc_p.val * np.pi/180
        self.x_gc[5] = self.slider_x_gc_h.val * np.pi/180
        camera = plu.cv.Camera(self.x_gc, self.K)

        args = {'K' : self.K, 'x_gc_true' : self.x_gc, 'corners' : self.corners}

        corners_global = plu.cv.homogeneous.dehomogenize(plu.coord_xfms.xyzrph2matrix(self.x_gbox).dot(plu.cv.homogeneous.homogenize(self.corners)))

        corners_uv = camera.project(corners_global)
        self.set_corners = corners_uv[:,self.face_of_interest]

        self.update()

    def run(self):
        self.button.on_clicked(self.run_monte_carlo)
        self.button_re.on_clicked(self.update_set_corners)

        self.slider_x_gc_x.on_changed(self.update)
        self.slider_x_gc_y.on_changed(self.update)
        self.slider_x_gc_z.on_changed(self.update)
        self.slider_x_gc_r.on_changed(self.update)
        self.slider_x_gc_p.on_changed(self.update)
        self.slider_x_gc_h.on_changed(self.update)

        self.slider_std_x.on_changed(self.update)
        self.slider_std_y.on_changed(self.update)
        self.slider_std_z.on_changed(self.update)
        self.slider_std_r.on_changed(self.update)
        self.slider_std_p.on_changed(self.update)
        self.slider_std_h.on_changed(self.update)

        self.update()
        plt.show()

s = Self(WIDTH, HEIGHT, DEPTH, TOP_FACE)
s.run()
