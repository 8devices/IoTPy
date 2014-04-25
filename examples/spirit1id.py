from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.spi import SPI
from IoTPy.pyuper.gpio import GPIO
from IoTPy.pyuper.utils import IoTPy_APIError, die

try:
	u = IoBoard()
except IoTPy_APIError, e: # seems can't establish connection with the UPER board
	details = e.args[0]
	die(details)

with u.get_pin(GPIO, 18) as sdn, u.get_pin(GPIO, 1) as csn, SPI(u,1) as spi_port:
    sdn.mode(GPIO.OUTPUT)
    sdn.write(0)
    csn.mode(GPIO.OUTPUT)
    csn.write(0)
    result = spi_port.transaction('\x01\xF0\x00\x00', 1)
    csn.write(1)
    print "rezult len:", len(result)
    print "%r" % result
    print result

