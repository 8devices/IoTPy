from _warnings import warn
from fcntl import ioctl
import struct
import subprocess
import array

from IoTPy.core.gpio import GPIOProducer
from IoTPy.core.spi import SPI, SPIProducer
from IoTPy.linux.gpio import LinuxGPIO
from IoTPy.linux.ioctl_def import IOW
from IoTPy.pycarambola2.spi import Carambola2_SPI


class Carambola2(GPIOProducer, SPIProducer):

    gpio_names = [1, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    def __init__(self):
        pass

    def __enter__(self):
        self._caramiot = None
        try:
            self._caramiot_file = open("/dev/caramiot", "r")
            self._caramiot = Caramiot(self._caramiot_file)
        except IOError:
            warn("Could not load caramiot driver. You will not be able to use some of the Carambola2 features.")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._caramiot:
            self._caramiot_file.close()

    def execute(self, cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate()

        return proc.returncode, out, err

    def GPIO(self, name, *args, **kwargs):
        if name not in self.gpio_names:
            raise ValueError("Invalid GPIO name %s. Must be one of %s." % (name, ", ".join(self.gpio_names)))

        return LinuxGPIO(name)
    
    def SPI(self, name, clock=1000000, mode=SPI.MODE_0, *args, **kwargs):
        if not self._caramiot:
            raise RuntimeError("Can't create SPI: caramiot driver not loaded.")

        if name not in self.gpio_names:
            raise ValueError("Invalid SPI CS name %s. Must be one of %s." % (name, ", ".join(self.gpio_names)))

        return Carambola2_SPI(self._caramiot, clock, mode, cs=name)


class Caramiot(object):

    CARAMIOT_MAGIC = ord('\xC2')
    CARAMIOT_IOC_SPI_INIT = IOW(CARAMIOT_MAGIC, 9, 4)
    CARAMIOT_IOC_SPI_CLEAN = IOW(CARAMIOT_MAGIC, 10, 4)

    def __init__(self, file):
        self._file = file

    def create_spi(self, clock, mode, cs):
        spi_init = struct.pack("@IBB", clock, mode, cs)
        spi_init = array.array('b', spi_init)

        try:
            ioctl(self._file, Caramiot.CARAMIOT_IOC_SPI_INIT, spi_init, True)
        except:
            return False

        return True

    def destroy_spi(self, cs):
        ioctl(self._file, Caramiot.CARAMIOT_IOC_SPI_CLEAN, cs)
