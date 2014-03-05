from pyuper.uperio import UperIO
from pyuper.i2c import i2c
from pyuper.utils import UPER_APIError, die
from things.si7020 import Si7020
from time import sleep

try:
	u = UperIO()
except UPER_APIError, e: # seems can't establish connection with the UPER board
	details = e.args[0]
	die(details)

with Si7020(i2c(u)) as sensor:
	for i in range(100):
		try:
			print "t = %4.2fC " % sensor.temperature(),
			print "RH= %4.2f%%" % sensor.humidity()
		except UPER_APIError:
			die("Temperature/humidity sensor reading error, exiting.")
		sleep(0.2)