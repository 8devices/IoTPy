from time import sleep
from IoTPy.linux.spi import SPIDEV


class Carambola2_SPI(SPIDEV):

    def __init__(self, caramiot, clock, mode, cs):
        super(Carambola2_SPI, self).__init__('/dev/spidev0.%d' % cs)

        self._caramiot = caramiot
        self.clock = clock
        self.mode = mode
        self.cs = cs

    def __enter__(self):
        if not self._caramiot.create_spi(self.clock, self.mode, self.cs):
            raise RuntimeError("Could not create new SPI device.")

        sleep(0.1)  # sometimes spidev doesn't open if called immediately after ioctl SPI_INIT

        return super(Carambola2_SPI, self).__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super(Carambola2_SPI, self).__exit__(exc_type, exc_val, exc_tb)
        self._caramiot.destroy_spi(self.cs)
