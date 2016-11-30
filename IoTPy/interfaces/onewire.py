from IoTPy.errors import IoTPy_APIError
from IoTPy.pinmaps import CAP_GPIO
from IoTPy.sfp import encode_sfp


class OneWire(object):

    def __init__(self, board, pin):
        self.board = board
        if self.board.pinout[pin].capabilities & CAP_GPIO:
            self.logical_pin = self.board.pinout[pin].pinID
        else:
            raise IoTPy_APIError("Trying to assign OneWire function to non GPIO pin.")

        #self.board.low_level_io(0, encode_sfp(1, [self.logical_pin]))  # set primary
        #self.board.low_level_io(0, encode_sfp(3, [self.logical_pin, 1])) # gpio mode output
        self.board.low_level_io(0, encode_sfp(100, [self.logical_pin]))

    def __enter__(self):
        return self

    def trans(self, data):
        self.board.low_level_io(0, encode_sfp(101, [data]))

    def __exit__(self, exc_type, exc_value, traceback):
        pass
