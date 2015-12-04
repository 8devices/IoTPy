from struct import unpack
from IoTPy.errors import IoTPy_ThingError


SI70xx_CMD_RH_HOLD      = b'\xE5'  # RH hold master mode
SI70xx_CMD_RH_NOHOLD    = b'\xF5'  # RH no hold master mode
SI70xx_CMD_TEMP_HOLD    = b'\xE3'  # temp hold master mode
SI70xx_CMD_TEMP_NOHOLD  = b'\xF3'  # temp no hold master mode
SI70xx_CMD_ANALOG       = b'\xEE'  #
SI70xx_CMD_TEMP_PREVIOUS= b'\xE0'  # temp from previous measurement

SI70xx_CMD_RESET        = b'\xFE'  # reset

SI70xx_CMD_WRITE_REG1   = b'\xE6'  # write user register 1 (RH/T setup)
SI70xx_CMD_READ_REG1    = b'\xE7'  # read user register 1 (RH/T setup)
SI70xx_CMD_WRITE_REG2   = b'\x50'  # write user register 2 (Analog setup)
SI70xx_CMD_READ_REG2    = b'\x10'  # read user register 2 (Analog setup)
SI70xx_CMD_WRITE_REG3   = b'\x51'  # write user register 3 (Heater setup)
SI70xx_CMD_READ_REG3    = b'\x11'  # read user register 3 (Heater setup)
SI70xx_CMD_WRITE_TCC    = b'\xC5'  # write thermistor correction coefficient
SI70xx_CMD_READ_TCC     = b'\x84'  # read thermistor correction coefficient

SI70xx_CMD_READ_ID1     = b'\xFA\x0F'  # read ID 1st byte
SI70xx_CMD_READ_ID2     = b'\xFC\xC9'  # read ID 2nd byte
SI70xx_CMD_FW_REVISION  = b'\x84\xB8'  # get firmware revision


class Si7013:
    """
    Si7013 humidity and temperature sensor class.

    :param interface:  I2C communication interface.
    :type interface: :class:`IoTPy.pyuper.i2c.I2C`
    :param int address: Si7013 sensor I2C address. Optional, default 0x40 (64)
    """

    def __init__(self, interface, address=0x40):
        self.interface = interface
        self.address = address

    def __enter__(self):
        return self

    def temperature(self):
        """
        Read, convert and return temperature.

        :return: Temperature value in celsius.
        :rtype: float
        :raise: IoTPy_ThingError
        """
        try:
            data, err = self.interface.transaction(self.address, SI70xx_CMD_TEMP_HOLD, 2)
            result_integer = unpack('>H', data[:2])[0]
            temp = (175.72 * result_integer)/65536 - 46.85
        except IoTPy_ThingError:
            raise IoTPy_ThingError("Si7020 - temperature reading error.")
        return temp

    def humidity(self):
        """
        Read, convert and return humidity.

        :return: Humidity value in percent.
        :rtype: float
        :raise: IoTPy_ThingError
        """
        try:
            data, err = self.interface.transaction(self.address, SI70xx_CMD_RH_HOLD, 2)
            result_integer = unpack('>H', data[:2])[0]
            rh = (125.0 * result_integer)/65536 - 6
        except IoTPy_ThingError:
            raise IoTPy_ThingError("Si7020 - humidity reading error.")
        return rh

    def analog(self):
        """
        Read, convert and return analog sensor value.

        :return: Analog ADC value
        :rtype: int
        :raise: IoTPy_ThingError
        """
        try:
            data, err = self.interface.transaction(self.address, SI70xx_CMD_ANALOG, 2)
            result_integer = unpack('>H', data[:2])[0]
            return result_integer
        except IoTPy_ThingError:
            raise IoTPy_ThingError("Si7020 - analog reading error.")

    def __exit__(self, ex_type, ex_value, traceback):
        pass


class Si7020:
    """
    Si7020 humidity and temperature sensor class.

    :param interface:  I2C communication interface.
    :type interface: :class:`IoTPy.pyuper.i2c.I2C`
    :param int address: Si7020 sensor I2C address. Optional, default 0x40 (64)
    """

    def __init__(self, interface, address=0x40):
        self.interface = interface
        self.address = address

    def __enter__(self):
        return self

    def temperature(self):
        """
        Read, convert and return temperature.

        :return: Temperature value in celsius.
        :rtype: float
        :raise: IoTPy_ThingError
        """
        try:
            data, err = self.interface.transaction(self.address, SI70xx_CMD_TEMP_HOLD, 2)
            result_integer = unpack('>H', data[:2])[0]
            temp = (175.72 * result_integer)/65536 - 46.85
        except IoTPy_ThingError:
            raise IoTPy_ThingError("Si7020 - temperature reading error.")
        return temp

    def humidity(self):
        """
        Read, convert and return humidity.

        :return: Humidity value in percent.
        :rtype: float
        :raise: IoTPy_ThingError
        """
        try:
            data, err = self.interface.transaction(self.address, SI70xx_CMD_RH_HOLD, 2)
            result_integer = unpack('>H', data[:2])[0]
            rh = (125.0 * result_integer)/65536 - 6
        except IoTPy_ThingError:
            raise IoTPy_ThingError("Si7020 - humidity reading error.")
        return rh

    def __exit__(self, ex_type, ex_value, traceback):
        pass