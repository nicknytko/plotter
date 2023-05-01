from plotter import Plotter
import numpy as np

plot = Plotter()
plot.home()

theta = np.linspace(0, 2 * np.pi, 64)
plot.plot(np.cos(theta) * 64.0, np.sin(theta) * 64.0)

plot.home()
