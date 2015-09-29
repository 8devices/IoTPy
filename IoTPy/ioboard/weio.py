from IoTPy.ioboard.ioboard import IoBoard
from IoTPy.ioboard.pinouts import WEIO_PINOUT


class WeIO(IoBoard):

    def __init__(self, serial_port=None):
        IoBoard.__init__(self, WEIO_PINOUT, serial_port)
