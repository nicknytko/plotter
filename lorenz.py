from plotter import Plotter
import numpy as np
from scipy.integrate import solve_ivp

plot = Plotter()
plot.home()

# Lorenz system parameters (taken from the Wikipedia example)
sigma = 10.
beta = 8./3.
rho = 28.

def f(t, a):
    a1, a2, a3 = a

    return np.array([
        -sigma * a1 + sigma * a2,
        rho * a1 - a2 - a1*a3,
        -beta * a3 + a1*a2
    ])

ode_sol = solve_ivp(f, (0, 100), np.ones(3), max_step=0.01)
y = ode_sol.y * 3.5 # scale coordinates

plot.plot(y[0], y[1])
plot.home()
