from time import sleep
from IoTPy.pyuper.utils import IoTPy_ThingError, die
from IoTPy.pyuper.i2c import I2C
from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.things.si70xx import Si7020
from IoTPy.things.am2321 import AM2321


with IoBoard() as u, AM2321(I2C(u)) as sensor, Si7020(I2C(u)) as other_sensor:
    print "UID", hex(sensor.read_uid())
    for i in xrange(10):
        try:
            print "----------------------------------"
            print "Si7020 t = %4.2fC RH= %4.2f%%" % (other_sensor.temperature(), other_sensor.humidity())
            sleep(0.5)
            sensor.read()
            print "AM2321 t = %4.2fC RH= %4.2f%%" % (sensor.temperature, sensor.humidity)
        except IoTPy_ThingError:
            pass
            die("Temperature/humidity sensor reading error, exiting.")
        sleep(0.5)