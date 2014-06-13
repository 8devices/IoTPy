from time import sleep

from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.i2c import I2C
from IoTPy.pyuper.utils import IoTPy_APIError, die
from IoTPy.things.si70xx import Si7020


try:
	u = IoBoard()
except IoTPy_APIError, e: # seems can't establish connection with the UPER board
	details = e.args[0]
	die(details)

with Si7020(I2C(u)) as sensor:
	for i in xrange(100):
		try:
			print "t = %4.2fC " % sensor.temperature(),
			print "RH= %4.2f%%" % sensor.humidity()
		except IoTPy_APIError:
			die("Temperature/humidity sensor reading error, exiting.")
		sleep(0.2)