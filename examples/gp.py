#!/usr/bin/env python

# --------------------------------------------------------------------------------

# "Gaussian Process Implicit Sufraces" 2D example, based on the work from Williams and
# Fitzgibbon, 2006

# --------------------------------------------------------------------------------

from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import scipy.interpolate
import PylabUtils as plu
import numpy

# collect data via mouse-clicks
def getTrainingData ():

    XMIN, XMAX = -10, 10
    YMIN, YMAX = XMIN, XMAX

    fig = figure ()
    ax = fig.add_subplot (111)
    axis ([XMIN, XMAX, YMIN, YMAX])

    print 'Select 1 interior point'
    interior = array (ginput (1, timeout=-1)[0])

    plot (interior[0], interior[1], 'r^', markersize=12)
    draw ()

    NOBS = 25
    print 'Select %d surface points' % (NOBS)
    surfaceObs = ginput (NOBS, timeout=-1)
    x = array (map (lambda x: x[0], surfaceObs))
    y = array (map (lambda x: x[1], surfaceObs))
    plot (x, y, 'bo', markersize=12)
    draw ()

    radii = []
    for pointIdx in range (NOBS):
        radius = norm (interior - array ([x[pointIdx], y[pointIdx]]))
        radii.append (radius)

    maxRadIdx = argmax (radii)
    maxRad = 2*radii[maxRadIdx]
    center = interior
    theta = linspace (0, 2*pi, 10)
    s, c = sin (theta), cos (theta)
    exterior = row_stack ((c*maxRad + interior[0], s*maxRad + interior[1]))

    plot (exterior[0,:], exterior[1,:], 'kv', markersize=12)
    axis ('equal')
    grid ('on')
    draw ()
    draw ()
    draw ()

    t = concatenate (([1], zeros (NOBS,), -1*ones (exterior.shape[1],)))
    xs = column_stack ((interior, row_stack ((x, y)), exterior))
    return (xs, t)

x, t = getTrainingData ()

# Stack pixels in a 2D mesh
N = 30
xCoords = linspace (min (x[0,:]), max (x[0,:]), N)
yCoords = linspace (min (x[1,:]), max (x[1,:]), N)
xxCoords, yyCoords = meshgrid (xCoords, yCoords)
xTest = row_stack ((xxCoords.reshape (N**2,), yyCoords.reshape (N**2),))

# Start GP regression using thin-plate kernel
# single kernel parameter: radius
theta = .1                      
# Gaussian additive noise, assumed independent but can have different variances
noise = ones (x.shape[1]) * 0.01
gp = plu.ml.GaussianProcessRegressionDense (plu.ml.kernels.thinPlate2D, theta, noise, x, t)
print 'Computing K (Gramian matrix)'
plu.misc.tic ()
gp.train ()
print 'done'
plu.misc.toc ()

print 'Computing estimate of GP mean'
plu.misc.tic ()
tTest = gp.predictAt (xTest).reshape (N, N)
print 'done'
plu.misc.toc ()

# Plot the regression, surface is curve where tTest == 0
imshow (tTest, origin='lower', 
        extent=[min (x[0,:]), max (x[0,:]), min (x[1,:]), max (x[1,:])], 
        cmap=cm.jet,
        interpolation='bilinear')
draw ()
colorbar ()
draw ()

# plot surface using lots of interpolation and black pixels
interpolator = scipy.interpolate.RectBivariateSpline (xCoords, yCoords, tTest)
xCoordsInterp = linspace (min (x[0,:]), max (x[0,:]), 50*N)
yCoordsInterp = linspace (min (x[1,:]), max (x[1,:]), 50*N)
tTestInterp = interpolator (xCoordsInterp, yCoordsInterp)
grad1, grad2 = gradient (sign (tTestInterp))
edge = abs (grad1) + abs (grad2)
rowInds, colInds = plu.misc.find2 (edge != 0)
plot (xCoordsInterp[colInds], yCoordsInterp[rowInds], 'k,')
draw ()

fig = figure ()
ax = fig.add_subplot (111, projection='3d')
ax.plot_surface (xxCoords, yyCoords, tTest, rstride=1, cstride=1, cmap=cm.jet)
draw ()
hold ('on')
z = zeros (tTest.shape)
ax.plot_wireframe (xxCoords, yyCoords, z)

show ()
