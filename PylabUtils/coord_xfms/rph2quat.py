import dofs

import numpy

def rph2quat (rph):
    """

    Return the quaternion as a length-4 array from the
    length-3 array of Euler angles (roll-pitch-heading)

    """
    quat = numpy.zeros ((4,))
    roll, pitch, yaw = (rph[0], rph[1], rph[2])

    halfroll = roll / 2;
    halfpitch = pitch / 2;
    halfyaw = yaw / 2;

    sin_r2 = numpy.sin (halfroll);
    sin_p2 = numpy.sin (halfpitch);
    sin_y2 = numpy.sin (halfyaw);

    cos_r2 = numpy.cos (halfroll);
    cos_p2 = numpy.cos (halfpitch);
    cos_y2 = numpy.cos (halfyaw);

    quat[0] = cos_r2 * cos_p2 * cos_y2 + sin_r2 * sin_p2 * sin_y2;
    quat[1] = sin_r2 * cos_p2 * cos_y2 - cos_r2 * sin_p2 * sin_y2;
    quat[2] = cos_r2 * sin_p2 * cos_y2 + sin_r2 * cos_p2 * sin_y2;
    quat[3] = cos_r2 * cos_p2 * sin_y2 - sin_r2 * sin_p2 * cos_y2;

    return quat;
