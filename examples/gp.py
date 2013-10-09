#!/usr/bin/env python

# --------------------------------------------------------------------------------

# "Gaussian Process Implicit Sufraces" 2D example, based on the work from Williams and
# Fitzgibbon, 2006

# --------------------------------------------------------------------------------

from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import scipy.interpolate, scipy.stats
import PylabUtils as plu
import numpy
import os

betaInv = .00010
betaInv2 = .000010
NOBS = 25
NEXTERIOR = 10

# collect data via mouse-clicks
def getTrainingData ():

    XMIN, XMAX = -1, 1
    YMIN, YMAX = XMIN, XMAX

    fig = figure ()
    ax = fig.add_subplot (111)
    axis ([XMIN, XMAX, YMIN, YMAX])

    print 'Select 1 interior point'
    interior = array (ginput (1, timeout=-1)[0])

    plot (interior[0], interior[1], 'r^', markersize=12)
    draw ()

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
    maxRad = 1.3*radii[maxRadIdx]
    center = interior
    theta = linspace (0, 2*pi, NEXTERIOR)
    s, c = sin (theta), cos (theta)
    exterior = row_stack ((c*maxRad + interior[0], s*maxRad + interior[1]))

    # t = zeros (NOBS,)
    # xs = row_stack ((x, y))
    # noise = betaInv*ones (NOBS,)
    t = concatenate (([1], zeros (NOBS,), -1*ones (NEXTERIOR,)))
    xs = column_stack ((interior, row_stack ((x, y)), exterior))
    noise = concatenate (([betaInv2], betaInv*ones (NOBS,), betaInv2*ones (NEXTERIOR)))
    return (xs, t, noise, fig)

x, t, noise, firstFig = getTrainingData ()

inds = find (abs (t) < .1)
plot (x[0,inds], x[1,inds], 'bo', markersize=12)
axis ('equal')
grid ('on')
draw ()
draw ()
draw ()

# Stack pixels in a 2D mesh
N = 30
xCoords = linspace (min (x[0,:]), max (x[0,:]), N)
yCoords = linspace (min (x[1,:]), max (x[1,:]), N)
xxCoords, yyCoords = meshgrid (xCoords, yCoords)
xTest = row_stack ((xxCoords.reshape (N**2,), yyCoords.reshape (N**2),))

# Start GP regression using thin-plate kernel
# run gp for thinplate and squared exponential kernels
thetaThinPlate = norm (array ([min (x[0,:]), min (x[1,:])]) - array ([max (x[0,:]), max (x[1,:])]))
thetaSqExp = 0.1
gpThinPlate = plu.ml.GaussianProcessRegressionDense (plu.ml.kernels.thinPlate2D, thetaThinPlate, noise, x, t)
gpSqExp = plu.ml.GaussianProcessRegressionDense (plu.ml.kernels.sqExp, thetaSqExp, noise, x, t)

thetas = [thetaThinPlate, thetaSqExp]
gps = [gpThinPlate, gpSqExp]
biases = [0, -1]
for theta, gp, bias in zip (thetas, gps, biases):
    print 'Computing K (Gramian matrix)'
    plu.misc.tic ()
    gp.train ()
    print 'done'
    plu.misc.toc ()

    print 'Computing estimate of GP mean'
    plu.misc.tic ()
    tTestFlat = gp.predictAt (xTest, bias=bias)
    tTestSigmaFlat = gp.sigmaAt (xTest, ones (xTest.shape[1]) * .01)
    tTest = tTestFlat.reshape (N, N)
    tTestSigma = tTestSigmaFlat.reshape (N, N)
    print 'done'
    plu.misc.toc ()

    # Plot the regression, surface is curve where tTest == 0
    figure ()
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
    ax.plot_wireframe (xxCoords, yyCoords, tTest + tTestSigma, color='r')
    ax.plot_wireframe (xxCoords, yyCoords, tTest - tTestSigma, color='b')

    figure ()
    imshow ((scipy.stats.norm.pdf (0, loc=tTestFlat, scale=tTestSigmaFlat)).reshape(N,N), origin='lower', 
            extent=[min (x[0,:]), max (x[0,:]), min (x[1,:]), max (x[1,:])], 
            cmap=cm.gray_r,
            interpolation='bilinear')
    colorbar ()
    draw ()

show ()
