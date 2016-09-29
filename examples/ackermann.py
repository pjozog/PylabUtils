#!/usr/bin/env python

from pylab import *

import PylabUtils as plu
import scipy.linalg

class Ackermann():
    def __init__(self, dt):
        self.kAlpha           = 2.16
        self.kGearRatio       = 9e-03
        self.kOversteerFactor = 1e-03
        self.kTiny            = 0.0001
        self.dt               = dt

    def x_i_iplus1(self, x, **kwargs):
        steer_angle = x[0]
        wheel_speed_l = x[1]
        wheel_speed_r = x[2]

        speed = 0.5*(wheel_speed_l + wheel_speed_r)
        angle = self.kGearRatio*steer_angle / (1. + self.kOversteerFactor*speed*speed)

        x = speed*self.dt
        y = 0.
        theta = plu.misc.minimizedAngle(0. + self.kAlpha*self.dt*speed*tan(angle));
        return np.array([x, y, theta])

# Shows how to scale time to maintain same distribution with varying timesteps
if __name__ == '__main__':
    dt = 0.1                   # time between sensor readings, e.g., changeable
    a = Ackermann(dt)
    ackermannSigma = eye(3)

    ackermannSigma[0,0] = (10)**2
    ackermannSigma[1,1] = (0.01)**2
    ackermannSigma[2,2] = (0.01)**2
    ackermannSigma /= dt        # need to scale covariance by time!

    plt.ion()

    x_gi = np.array([0., 0., 0., 0., 0., 0.])
    x_gi_cov = np.zeros((6,6))
    xs = []
    ys = []

    steer_angle = 920 * pi/180.
    wheel_speed_l = 0.1     # m/s
    wheel_speed_r = 0.1     # m/s
    x = np.array([steer_angle, wheel_speed_l, wheel_speed_r])
    J = plu.diff.numerical_jacobian(a.x_i_iplus1, x)

    sigmaPoints, meanWeight, covWeight = plu.ut.unscented_transform (x, ackermannSigma)

    mu = a.x_i_iplus1(x)
    Sigma_ = J.dot(ackermannSigma).dot(J.T)

    mu, Sigma_ = plu.ut.unscented_func(a.x_i_iplus1, sigmaPoints, meanWeight,
                                       covWeight, angleMask=np.array([False, False, True]))

    maxsecs = 10                # number of seconds to execute, changeable
    N = int(maxsecs / dt)       # number of discrete steps to compute
    for i in range(N):
        Sigma = np.zeros((6,6))
        Sigma[0:2,0:2] = Sigma_[0:2,0:2]
        Sigma[5,5] = Sigma_[2,2]
        Sigma[5,0] = Sigma_[2,0]
        Sigma[0,5] = Sigma_[0,2]
        Sigma[5,1] = Sigma_[2,1]
        Sigma[1,5] = Sigma_[1,2]

        x_i_iplus1 = np.array([mu[0], mu[1], 0., 0., 0., mu[2]])
        x_gi = plu.coord_xfms.ssc.head2tail(x_gi, x_i_iplus1)

        JOdom = plu.coord_xfms.ssc.head2tail_jacob(x_gi, x_i_iplus1)
        x_gi_cov = JOdom.dot(scipy.linalg.block_diag(x_gi_cov, Sigma)).dot(JOdom.T)

        plt.clf()

        xs.append(x_gi[0])
        ys.append(x_gi[1])

        plot(xs, ys)

        x_gi_2d = np.array([x_gi[0], x_gi[1], x_gi[2]])

        xcov, ycov = plu.plotting.calculateEllipseXY(x_gi[0:2], x_gi_cov[0:2,0:2], 9, 100)
        plot(xcov, ycov)
        plot(x_gi[0], x_gi[1], 'x')
        axis('equal')
        grid('on')
        gca().set_ylim([-2, 2])
        gca().set_xlim([-2, 2])
        plt.pause(0.0001)

plt.pause(0)
show()
