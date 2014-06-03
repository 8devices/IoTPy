"""
Simple example of using SRF08 ultrasonic range finder UPER thing module

"""

from time import sleep

from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.i2c import I2C
from IoTPy.pyuper.utils import IoTPy_ThingError, IoTPy_APIError, IoTPy_IOError, errmsg, die
from IoTPy.things.srf08 import Srf08


try:
    with IoBoard() as u, Srf08(I2C(u)) as sensor:
        for i in xrange(10):
            try:
                print "distance: %3dcm" % sensor.distance(Srf08.CM),
                print "light:", sensor.light()
            except IoTPy_ThingError:
                die("Distance/Light sensor reading error, exiting")
            sleep(0.2)
        sensor.change_address(0x74)
        print "------------sensor address changed------------"
        for i in xrange(10):
            try:
                print "distance: %3dcm" % sensor.distance(Srf08.CM),
                print "light:", sensor.light()
            except IoTPy_ThingError:
                die("Distance/Light sensor reading error, exiting")
            sleep(0.2)
        sensor.change_address(0x70)
        print "------------sensor address changed------------"
        for i in xrange(10):
            try:
                print "distance: %3dcm" % sensor.distance(Srf08.CM),
                print "light:", sensor.light()
            except IoTPy_ThingError:
                die("Distance/Light sensor reading error, exiting")
            sleep(0.2)
except (IoTPy_IOError, IoTPy_APIError), e: # don't see the I2C buss or UPER board
    details = e.args[0]
    die(details)
except KeyboardInterrupt:
    errmsg("CTRL/C pressed, exiting.")
    exit(1)