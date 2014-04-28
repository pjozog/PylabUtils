#!/usr/bin/env python

def margcov (Sigma, variables):
    return Sigma[variables,:][:,variables]
