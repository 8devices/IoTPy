import ctypes
from fcntl import ioctl
import struct
import array
from IoTPy.core.spi import SPI
from IoTPy.linux.ioctl_def import IOW


class SPIDEV(SPI):

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self._file = open(self.name, "w+")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()

    def read(self, count, value=0):
        return self._file.read(count)

    def write(self, data):
        self._file.write(data)
        self._file.flush()

    def transaction(self, data_out):
        size = len(data_out)
        buf = ctypes.c_buffer(data_out, size)

        txfer = struct.pack("@QQIIHBBxxxx", ctypes.addressof(buf), ctypes.addressof(buf), size, 0, 0, 8, 0)
        txfer = array.array('b', txfer)

        SPI_IOC_MAGIC = ord('k')
        SPI_IOC_MESSAGE = IOW(SPI_IOC_MAGIC, 0, 32)
        try:
            ioctl(self._file, SPI_IOC_MESSAGE, txfer, True)
        except:
            raise RuntimeError("Error while performing SPI transaction.")

        return ctypes.string_at(buf, size)