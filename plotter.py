import serial
import numpy as np

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
