from IoTPy.ioboard.ioboard import IoBoard
from IoTPy.ioboard.pinouts import _8dev2300_PINOUT


class _8dev2300(IoBoard):

    def __init__(self, serial_port=None):
        IoBoard.__init__(self, _8dev2300_PINOUT, serial_port)
