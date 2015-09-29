from IoTPy.ioboard.ioboard import IoBoard
from IoTPy.ioboard.pinouts import LPCExpresso11U14REVA_PINOUT


class LPCexpresso(IoBoard):

    def __init__(self, serial_port=None):
        IoBoard.__init__(self, LPCExpresso11U14REVA_PINOUT, serial_port)
