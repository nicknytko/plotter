from plotter import Plotter, Turtle, LSystem

plot = Plotter()
plot.home()

turtle = Turtle(plot)

# L-system for the Hilbert curve
hilbert = LSystem({
    'A': '+BF-AFA-FB+',
    'B': '-AF+BFB+FA-',
})

turtle.pen_down = True
turtle.follow_system(hilbert, 'A', iterations=7, scale=64)
turtle.pen_down = False

plot.home()
