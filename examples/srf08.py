"""
Simple example of using SRF08 ultrasonic range finder UPER thing module

"""

from pyuper.uperio import UperIO
from pyuper.i2c import i2c
from pyuper.utils import UPER_ThingError, UPER_APIError, UPER_IOError, errmsg, die
from things.srf08 import Srf08
from time import sleep


try:
	with UperIO() as u, Srf08(i2c(u)) as sensor:
		for i in range(100):
			try:
				print "distance: %3d" % sensor.distance(Srf08.CM), "cm,",
				print "light:", sensor.light()
			except UPER_ThingError:
				die("Distance/Light sensor reading error, exiting")
			sleep(0.2)
except (UPER_IOError, UPER_APIError), e: # don't see the I2C buss or UPER board
	details = e.args[0]
	die(details)
except KeyboardInterrupt:
	errmsg("CTRL/C pressed, exiting.")
	exit(1)