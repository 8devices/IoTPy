from IoTPy.ioboard.ioboard import IoBoard
from IoTPy.ioboard.pinouts import UPER1_PINOUT


class UPER1(IoBoard):

    def __init__(self, serial_port=None):
        IoBoard.__init__(self, UPER1_PINOUT, serial_port)
