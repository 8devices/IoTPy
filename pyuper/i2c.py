from utils import UPER_IOError, UPER_ThingError, UPER_APIError, errmsg
from types import IntType


class i2c:
    def __init__(self, board, port = 0, pins = []):
        self.board = board
        self.port = port
        self.pins = pins
        self.board.uper_io(0, self.board.encode_sfp(40, []))

    def __enter__(self):
        return self

    def transaction(self, address, write_data, read_length):
        try:
            result = self.board.decode_sfp(self.board.uper_io(1, self.board.encode_sfp(41, [address, write_data, read_length])))
        except UPER_APIError:
            errmsg("UPER API: I2C bus not connected.")
            raise UPER_IOError("I2C bus not connected.")
        if type(result[1][0]) == IntType:
            errmsg("UPER Interface: I2C device with address %#x returned error code %#x.", address, result[1][0] )
            raise UPER_ThingError("I2C slave reading error.")
        else:
            return result[1][0]

    def __exit__(self, exc_type, exc_value, traceback):
        self.board.uper_io(0, self.board.encode_sfp( 42, []))

