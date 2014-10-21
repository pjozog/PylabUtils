import numpy

def matrix2xyzrph (M):
    """

    Return the 6-dof pose from a 4x4 transformation matrix M
    
    """
    tx = M[0,3]
    ty = M[1,3]
    tz = M[2,3]
    rx = numpy.arctan2(M[2,1], M[2,2])
    ry = numpy.arctan2(-M[2,0], numpy.sqrt(M[0,0]*M[0,0] + M[1,0]*M[1,0]))
    rz = numpy.arctan2(M[1,0], M[0,0])
    x = numpy.array ([tx, ty, tz, rx, ry, rz])
    return x
