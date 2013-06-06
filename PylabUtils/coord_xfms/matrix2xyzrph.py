from pylab import *

def matrix2xyzrph (M):

    tx = M[0,3]
    ty = M[1,3]
    tz = M[2,3]
    rx = arctan2(M[2,1], M[2,2])
    ry = arctan2(-M[2,0], sqrt(M[0,0]*M[0,0] + M[1,0]*M[1,0]))
    rz = arctan2(M[1,0], M[0,0])
    x = array ([tx, ty, tz, rx, ry, rz])
    return x
