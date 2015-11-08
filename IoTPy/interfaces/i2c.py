from IoTPy.errors import IoTPy_IOError, IoTPy_APIError, errmsg
from IoTPy.sfp import encode_sfp, decode_sfp


class I2C(object):
    """
    I2C communication module.

    :param board: IoBoard with I2C capability.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param port: I2C module number
    :type port: int
    """

    def __init__(self, board, port=0):
        self.board = board
        self.port = port
        self.board.lowlevel_io(0, encode_sfp(40, []))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.board.lowlevel_io(0, encode_sfp(42, []))

    def scan(self):
        """
        Scan I2C interface for connected devices.

        :return: A list of active I2C device addresses.
        :rtype: list
        """
        dev_list = []
        for address in xrange(1, 128):
            try:
                result = self.board.lowlevel_io(1, encode_sfp(41, [address, '', 0]))
                if result[-1] == 'X':
                    dev_list.append(address)
            except IoTPy_APIError:
                errmsg("UPER API: I2C bus not connected.")
                raise IoTPy_IOError("I2C bus not connected.")
        return dev_list

    def read(self, address, count):
        return self.transaction(address, "", count)

    def write(self, address, data):
        return self.transaction(address, data, 0)

    def transaction(self, address, write_data, read_length):
        """
        Perform I2C data transaction.

        I2C data transaction consists of (optional) write transaction, followed by (optional) read transaction.

        :param address: I2C device address.
        :type address: int
        :param write_data: A byte sequence to be transmitted. If write_data is empty string, no write transaction \
         will be executed.
        :type write_data: str
        :param read_length: A number of bytes to be received. If read_length is 0, no read transaction will be executed.
        :type read_length: int
        :return: Received data and I2C transaction status/error code.
        :rtype: (str, int)
        :raise: IoTPy_APIError, IoTPy_ThingError
        """

        try:
            result = decode_sfp(self.board.lowlevel_io(1, encode_sfp(41, [address, write_data, read_length])))
        except IoTPy_APIError:
            errmsg("UPER API: I2C bus not connected.")
            raise IoTPy_IOError("I2C bus not connected.")

        return result[1][1], result[1][2]  # return read buffer and error
