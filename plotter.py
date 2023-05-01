import serial
import numpy as np
from time import sleep

class Plotter:
    def __init__(self,
                 tty_device='/dev/ttyUSB0',
                 tty_baud=115200):
        self.connection = serial.Serial(tty_device,
                                        tty_baud,
                                        timeout=60)
        self._xy = np.zeros(2)
        self._pen_up = True

    def __del__(self):
        self.connection.close()

    def send(self, msg):
        self.connection.write((msg + '\n').encode('ascii'))

    def recv(self):
        return self.connection.readline().decode('ascii').strip()

    def gcode(self, cmd):
        while True:
            self.send(cmd)

            ack = self.recv()
            if ack == 'ok':
                break
            if ack.startswith('error'):
                raise RuntimeError(f'Error received from device: {ack}')

    # Homing

    def home(self):
        self.pen_up = True
        self.gcode('G28')
        self._xy[:] = 0.

    # Plotter pen

    @property
    def pen_up(self):
        return self._pen_up

    @pen_up.setter
    def pen_up(self, val):
        self._pen_up = val
        if val:
            self.gcode('M5')
        else:
            self.gcode('M3 S1000')
        sleep(0.2)

    @property
    def pen_down(self):
        return not self._pen_up

    @pen_up.setter
    def pen_down(self, val):
        self.pen_up = not val

    # Plotter head position

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, val):
        self._xy[:] = val[:]
        self.gcode(f'G0 X{val[0]:.2f} Y{val[1]:.2f}')

    @property
    def x(self):
        return self._xy[0]

    @x.setter
    def x(self, val):
        self._xy[0] = val
        self.gcode(f'G0 X{val:.2f}')

    @property
    def y(self):
        return self._xy[1]

    @x.setter
    def y(self, val):
        self._xy[1] = val
        self.gcode(f'G0 Y{val:.2f}')

    # matplotlib style plotting
    def plot(self, x, y):
        assert(len(x) == len(y))

        # Move to first coordinate
        self.pen_down = False
        self.xy = np.array([x[0], y[0]])
        self.pen_down = True

        # Plot
        if len(x) > 1:
            for coord in np.column_stack((x[1:], y[1:])):
                self.xy = coord

        self.pen_down = False


class Turtle:
    '''
    Classic turtle-style graphics
    '''

    def __init__(self, plot):
        self.angle = 0
        self.plot = plot

    # Movement

    def forward(self, amount=1.0):
        self.plot.xy += np.array([np.cos(self.angle),
                                  np.sin(self.angle)]) * amount

    def backward(self, amount=1.0):
        self.forward(-amount)

    # Turning

    def left(self, degrees):
        self.angle += degrees * np.pi / 180

    def right(self, degrees):
        self.left(-degrees)

    # Drawing

    @property
    def pen_down(self):
        return self.plot.pen_down

    @pen_down.setter
    def pen_down(self, val):
        self.plot.pen_down = val

    @property
    def pen_up(self):
        return self.plot.pen_up

    @pen_up.setter
    def pen_up(self, val):
        self.plot.pen_up = val

    # L-System
    def follow_system(self, system, axiom,
                      iterations=1, scale=1.0,
                      left='+', right='-',
                      forward='F',
                      back=''):

        rule = system.rewrite(axiom, iterations)
        length = (2.0 ** -(iterations - 1)) * scale

        for symbol in rule:
            if symbol == left:
                self.left(90)
            elif symbol == right:
                self.right(90)
            elif symbol == forward:
                self.forward(length)
            elif symbol == back:
                self.backward(length)


class LSystem:
    def __init__(self, rules):
        self.rules = rules

    def _rewrite_once(self, axiom):
        out = ''
        for symbol in axiom:
            if symbol in self.rules:
                out += self.rules[symbol]
            else:
                out += symbol
        return out

    def rewrite(self, axiom, iterations=1):
        for i in range(iterations):
            axiom = self._rewrite_once(axiom)
        return axiom
