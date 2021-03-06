#!/usr/bin/env python

from . import regression

from pylab import zeros, solve, diag, eye, sqrt

class GaussianProcessRegression (regression.Regression):
    def __init__ (self, kernel, theta, trainNoise, trainData, trainLabels):
        self._kernel = kernel
        self._theta = theta
        assert (len (trainLabels.shape) == 1)
        self.trainLabels = trainLabels.copy ()
        self.trainData = trainData.copy ()
        self.trainNoise = trainNoise

    def predictAt (self, X, **kwargs):
        numTestLabels = X.shape[1]
        numTrainlabels = self.trainData.shape[1]
        t = zeros (numTestLabels)
        bias = kwargs.get ('bias', 0)
        for i in range (numTestLabels):
            k = self._k (X[:,i])
            t[i] = k.dot (solve (self.K, self.trainLabels - bias)) + bias
        return t

    def sigmaAt (self, X, noises):
        numTestLabels = X.shape[1]
        numTrainlabels = self.trainData.shape[1]
        sigmas = zeros (numTestLabels)
        for i in range (numTestLabels):
            c = self._kernel (X[:,i], X[:,i], self._theta) + noises[i]
            k = self._k (X[:,i])
            sigmas[i] = c - k.dot (solve (self.K, k))
        return sqrt (sigmas)

    def train (self):
        self.K = self._K () + diag (self.trainNoise)

    def _K (self):
        raise NotImplementedError ("GP K (Gram matrix) computation not yet implemented")

    def _k (self, x):
        raise NotImplementedError ("GP k vector computation not yet implemented")

class GaussianProcessRegressionDense (GaussianProcessRegression):

    def __init__(self, kernel, theta, trainNoise, trainData, trainLabels):
        GaussianProcessRegression.__init__ (self, kernel, theta, trainNoise, trainData, trainLabels)

    def _K (self):
        numLabels = self.trainData.shape[1]
        K = zeros ((numLabels, numLabels))
        for i in range (numLabels):
            for j in range (numLabels):
                K[i,j] = self._kernel (self.trainData[:,i], self.trainData[:,j], self._theta)
                K[j,i] = K[i,j]
        return K

    def _k (self, x):
        numLabels = self.trainData.shape[1]
        k = zeros (numLabels,)
        for i in range (numLabels):
            k[i] = self._kernel (self.trainData[:,i], x, self._theta)
        return k

class GaussianProcessRegressionSparse (GaussianProcessRegression):

    def __init__(self, kernel, theta, trainNoise, trainData, trainLabels):
        GaussianProcessRegression.__init__ (self, kernel, theta, trainNoise, trainData, trainLabels)
