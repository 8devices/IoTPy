from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.i2c import I2C
from IoTPy.pyuper.utils import IoTPy_APIError, IoTPy_IOError, die

try:
    with I2C(IoBoard()) as i2c_bus:
        print i2c_bus.scan()

except (IoTPy_IOError, IoTPy_APIError), e: # don't see the I2C bus or UPER board
    details = e.args[0]
    die(details)
