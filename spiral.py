from plotter import Plotter
import numpy as np

plot = Plotter()
plot.home()

def solve_ode(alpha, r0=64, dt=0.1, theta0=0.):
    # dtheta/dt = 1
    # dr/dt     = -r * alpha
    # integrate with forward Euler, returns xy coordinates

    thetas = [theta0]
    rs = [r0]

    while True:
        theta = thetas[-1] + 1. * dt
        r = rs[-1] + (-rs[-1] * alpha) * dt

        thetas.append(theta)
        rs.append(r)

        # Breaking conditions
        # if alpha == 0 => dr=0, then stop when we've done a revolution
        # otherwise, stop when r = 0
        if alpha == 0. and theta >= 2 * np.pi:
            break
        elif alpha != 0 and abs(r) < 1e-1:
            break

    thetas = np.array(thetas)
    rs = np.array(rs)

    return np.cos(thetas) * rs, np.sin(thetas) * rs

N = 16
radius = 64
dt = 0.1
thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)
alpha = 0.1

for theta in thetas:
    plot.plot(*solve_ode(alpha, radius, dt, theta))

plot.home()
