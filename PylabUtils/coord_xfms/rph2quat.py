#!/usr/bin/env python

from pylab import *
import dofs

def rph2quat (rph):
    quat = zeros ((4,))
    roll, pitch, yaw = (rph[0], rph[1], rph[2])

    halfroll = roll / 2;
    halfpitch = pitch / 2;
    halfyaw = yaw / 2;

    sin_r2 = sin (halfroll);
    sin_p2 = sin (halfpitch);
    sin_y2 = sin (halfyaw);

    cos_r2 = cos (halfroll);
    cos_p2 = cos (halfpitch);
    cos_y2 = cos (halfyaw);

    quat[0] = cos_r2 * cos_p2 * cos_y2 + sin_r2 * sin_p2 * sin_y2;
    quat[1] = sin_r2 * cos_p2 * cos_y2 - cos_r2 * sin_p2 * sin_y2;
    quat[2] = cos_r2 * sin_p2 * cos_y2 + sin_r2 * cos_p2 * sin_y2;
    quat[3] = cos_r2 * cos_p2 * sin_y2 - sin_r2 * sin_p2 * cos_y2;

    return quat;
