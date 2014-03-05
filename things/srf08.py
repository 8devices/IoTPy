from pyuper.utils import UPER_ThingError, errmsg
from time import sleep
from struct import unpack, pack


class Srf08:
    ADDRESS = 0x70        # Address of the SRF08
    CMD = '\x00'            # Command byte
    LIGHT = '\x01'          # Byte to read light sensor
    RESULT = '\x02'       	# Byte for start of ranging data
    GAIN_REGISTER = '\x00' 	#
    RANGE_LOCATION = '\xff' # return distance in cm
    INCH = '\x50' 	# return distance in cm
    CM = '\x51' 	# return distance in cm
    MS = '\x52' 	# return distance in cm

    def __init__(self, interface, sensor_address=ADDRESS):
        self.interface = interface
        self.address = sensor_address
        if sensor_address != Srf08.ADDRESS:
            self.interface.transaction(Srf08.ADDRESS, Srf08.CMD + '\xa0' + Srf08.GAIN_REGISTER + Srf08.RANGE_LOCATION, 0)
            self.interface.transaction(Srf08.ADDRESS, Srf08.CMD + '\xaa' + Srf08.GAIN_REGISTER + Srf08.RANGE_LOCATION, 0)
            self.interface.transaction(Srf08.ADDRESS, Srf08.CMD + '\xa5' + Srf08.GAIN_REGISTER + Srf08.RANGE_LOCATION, 0)
            bs = pack('I', sensor_address)
            self.interface.transaction(Srf08.ADDRESS, Srf08.CMD + bs + Srf08.GAIN_REGISTER + Srf08.RANGE_LOCATION, 0)

    def __enter__(self):
        return self

    def distance(self, distance_unit = CM):
        if distance_unit not in (Srf08.CM, Srf08.INCH, Srf08.MS):
            errmsg("Wrong units for distance, should be 'c' or 'i' or 'm'.")
            raise UPER_ThingError("Wrong units for distance, should be 'c' or 'i' or 'm'.")
        try:
            self.interface.transaction(self.address, Srf08.CMD + distance_unit, 0)
            sleep(0.08)
            distance = unpack('>H', self.interface.transaction(self.address, Srf08.RESULT, 2)[:2])[0]
        except UPER_ThingError:
            raise UPER_ThingError("srf08 - distance reading error.")
        return distance

    def light(self):
        try:
            self.interface.transaction(self.address, Srf08.CMD + Srf08.CM, 0)
            sleep(0.08)
            light = unpack('>B', self.interface.transaction(self.address, Srf08.LIGHT, 1)[:1])[0]
        except UPER_ThingError:
            raise UPER_ThingError("srf08 - distance reading error.")
        return light

    def get_revision(self):
        pass

    def __exit__(self, ex_type, ex_value, traceback):
        pass