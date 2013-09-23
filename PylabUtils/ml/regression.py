#!/usr/bin/env python

class Regression:
    
    def __init__ (self, trainData, trainLabels):
        self._trainData = trainData
        self._trainLabels = trainLabels

    def predictAt (self, x):
        raise NotImplementedError ('Label prediction not implemented')

    def train (self):
        raise NotImplementedError ('Regression training not implemented')
