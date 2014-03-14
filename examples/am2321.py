from pyuper.utils import UPER_ThingError, die
from pyuper.i2c import i2c
from pyuper.uperio import UperIO
from time import sleep
from things.si7020 import Si7020
from things.am2321 import AM2321

with UperIO() as u, AM2321(i2c(u)) as sensor, Si7020(i2c(u)) as other_sensor:
    print "UID", hex(sensor.read_uid())
    for i in range(10):
        try:
            print "----------------------------------"
            print "Si7020 t = %4.2fC RH= %4.2f%%" % (other_sensor.temperature(), other_sensor.humidity())
            sleep(0.5)
            sensor.read()
            print "AM2321 t = %4.2fC RH= %4.2f%%" % (sensor.temperature, sensor.humidity)
        except UPER_ThingError:
            pass
            die("Temperature/humidity sensor reading error, exiting.")
        sleep(0.5)