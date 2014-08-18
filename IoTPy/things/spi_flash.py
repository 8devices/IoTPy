import struct
from IoTPy.core.gpio import GPIO
from IoTPy.core.spi import SPI


class SPIFlash:

    def __init__(self, spi, cs):
        if not isinstance(spi, SPI):
            raise TypeError("spi argument must be of type SPI")

        if not isinstance(cs, GPIO):
            raise TypeError("cs argument must be of type GPIO")

        self.spi = spi
        self.cs = cs
        
    def __enter__(self):
        self.cs.setup(GPIO.OUTPUT)
        self.cs.write(GPIO.HIGH)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def write_enable(self):
        self.cs.write(GPIO.LOW)
        self.spi.write('\x06')
        self.cs.write(GPIO.HIGH)

    def write_disable(self):
        self.cs.write(GPIO.LOW)
        self.spi.write('\x04')
        self.cs.write(GPIO.HIGH)

    def read_status(self):
        self.cs.write(GPIO.LOW)
        buf = self.spi.transaction('\x05\x00')
        self.cs.write(GPIO.HIGH)
        status = struct.unpack('>xB', buf)
        return status[0]

    def write_status(self, status):
        buf = struct.pack(">BB", 0x01, status & 0xFF)
        self.cs.write(GPIO.LOW)
        self.spi.write(buf)
        self.cs.write(GPIO.HIGH)

    def read(self, address, count=1):
        buf = chr(0x03) + chr(address >> 16) + chr(address >> 8 & 0xFF) + chr(address & 0xFF) + '\xFF'*count

        self.cs.write(GPIO.LOW)
        data = self.spi.transaction(buf)
        self.cs.write(GPIO.HIGH)

        return data[4:]

    def page_program(self, address, data):
        buf = chr(0x02) + chr(address >> 16) + chr(address >> 8 & 0xFF) + chr(address & 0xFF) + data

        self.cs.write(GPIO.LOW)
        self.spi.write(buf)
        self.cs.write(GPIO.HIGH)

    def sector_erase(self, address):
        buf = chr(0x20) + chr(address >> 16) + chr(address >> 8 & 0xFF) + chr(address & 0xFF)

        self.cs.write(GPIO.LOW)
        self.spi.write(buf)
        self.cs.write(GPIO.HIGH)