from struct import unpack
from IoTPy.pyuper.utils import IoTPy_ThingError


class Lm75:
    ADDRESS = 0x48            # Address of the LM75

    def __init__(self, interface, address=ADDRESS):
        self.interface = interface
        self.address = address

    def __enter__(self):
        return self

    def temperature(self):
        try:
            result_raw = self.interface.transaction(self.address, '\x00', 2)
            result_integer = unpack('>H', result_raw)[0]
            temperature = result_integer / 256.0
        except IoTPy_ThingError:
            raise IoTPy_ThingError("LM75 - temperature reading error.")
        return temperature

    def __exit__(self, ex_type, ex_value, traceback):
        pass
