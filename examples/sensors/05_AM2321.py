from time import sleep
from IoTPy.pyuper.i2c import I2C
from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.things.am2321 import AM2321

with IoBoard() as uper, I2C(uper) as i2c, AM2321(i2c) as sensor:
    while True:
        sensor.read()
        print "Temperature: %.1f Humidity: %.1f" % (sensor.temperature, sensor.humidity)
        sleep(1)