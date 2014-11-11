import ctypes
import fcntl
import struct
import array
from IoTPy.core.i2c import I2C


class LinuxI2C(I2C):

    I2C_RDWR = 0x0707

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self._file = open(self.name, "w+")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()

    def read(self, address, count):
        read_buf = ctypes.c_buffer("\0"*count, count)

        read_msg = struct.pack("@HHHP", address, 0x0001, count, ctypes.addressof(read_buf))
        msgs = ctypes.c_buffer(read_msg, len(read_msg))

        txfer = struct.pack("@PI", ctypes.addressof(msgs), 1)
        txfer = array.array('b', txfer)

        try:
            fcntl.ioctl(self._file, LinuxI2C.I2C_RDWR, txfer, True)
        except IOError as e:
            return "", e.errno

        return ctypes.string_at(read_buf, count), 0

    def write(self, address, data):
        write_buf = ctypes.c_buffer(data, len(data))

        write_msg = struct.pack("@HHHP", address, 0x0000, len(data), ctypes.addressof(write_buf))
        msgs = ctypes.c_buffer(write_msg, len(write_msg))

        txfer = struct.pack("@PI", ctypes.addressof(msgs), 1)
        txfer = array.array('b', txfer)

        try:
            fcntl.ioctl(self._file, LinuxI2C.I2C_RDWR, txfer, True)
        except IOError as e:
            return "", e.errno

        return "", 0

    def transaction(self, address, data, read_len):
        write_buf = ctypes.c_buffer(data, len(data))
        read_buf = ctypes.c_buffer("\0"*read_len, read_len)

        msg0 = struct.pack("@HHHP", address, 0x0000, len(data), ctypes.addressof(write_buf))
        msg1 = struct.pack("@HHHP", address, 0x0001, read_len, ctypes.addressof(read_buf))
        msgs = ctypes.c_buffer(msg0+msg1, len(msg0)+len(msg1))

        txfer = struct.pack("@PI", ctypes.addressof(msgs), 2)
        txfer = array.array('b', txfer)

        try:
            fcntl.ioctl(self._file, LinuxI2C.I2C_RDWR, txfer, True)
        except IOError as e:
            return "", e.errno

        return ctypes.string_at(read_buf, read_len), 0
