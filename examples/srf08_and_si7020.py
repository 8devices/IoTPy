from time import sleep

import  mosquitto

from IoTPy.things.si70xx import Si7020
from IoTPy.things.srf08 import Srf08
from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.i2c import I2C
from IoTPy.pyuper.utils import IoTPy_APIError, IoTPy_ThingError, IoTPy_IOError, die, errmsg


mqttc = mosquitto.Mosquitto()

mqttc.connect("test.mosquitto.org", 1883, 60)

die_on_error = False # if True, we will exit on sensor read error

try:
    with IoBoard() as u, I2C(u) as myi2c, Si7020(myi2c) as sensor1, Srf08(myi2c) as sensor2:
        for i in xrange(600):
            print"-----------------------------------------------",i
            try:
                temp = "t = %4.2fC " % sensor1.temperature()
                rh = "RH= %4.2f%%" % sensor1.humidity()
                print temp, rh
                mqttc.publish("8dev", temp + rh)

            except IoTPy_ThingError:
                if die_on_error:
                    die("Temperature/Humidity sensor reading error, exiting.")
                errmsg("Temperature/Humidity sensor reading error.")

            try:
                print "distance: %3dcm" % sensor2.distance(),
                print "light:", sensor2.light()
            except IoTPy_ThingError:
                if die_on_error:
                    die("Distance/Light sensor reading error, exiting")
                errmsg("Distance/Light sensor reading error.")
            sleep(1)
except (IoTPy_IOError, IoTPy_APIError), e: # don't see the I2C buss or UPER board
    details = e.args[0]
    die(details)
except KeyboardInterrupt:
    errmsg("CTRL/C pressed, exiting.")
    exit(1)
