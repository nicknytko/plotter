from plotter import *
import numpy as np
import opensimplex

plot = Plotter()
plot.home()

N = 40
scale = 64.
l = np.linspace(-1, 1, N)
xs, ys = np.meshgrid(l, l)

#opensimplex.seed(0)

def trace_ode(x, y, dt=0.01):
    xs = [x]
    ys = [y]

    tracing = True

    while tracing:
        x = xs[-1]
        y = ys[-1]

        dx = opensimplex.noise3(x, y, 1.0)
        dy = opensimplex.noise3(x, y, -1.0)

        x = x + dx * dt
        y = y + dy * dt

        if x < -1:
            tracing = False
            x = -1
        if x > 1:
            tracing = False
            x = 1
        if y < -1:
            tracing = False
            y = -1
        if y > 1:
            tracing = False
            y = 1
        if abs(x - xs[-1]) < 1e-4 and abs(y - ys[-1]) < 1e-4:
            tracing = False

        xs.append(x)
        ys.append(y)

    return np.array(xs) * scale, np.array(ys) * scale

xs = xs.flatten()
ys = ys.flatten()

for x, y in zip(xs, ys):
    xx, yy = trace_ode(x, y)
    plot.plot(xx, yy)

plot.home()
plot.close()
