from time import sleep

from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.interrupt import Interrupt
from IoTPy.pyuper.gpio import GPIO
from IoTPy.pyuper.adc import ADC
from IoTPy.pyuper.utils import IoTPy_APIError, die, errmsg


def call_back1():
	print "From call_back1..."
	try:
		red.write(0)
		sleep(0.2)
		red.write(1)
		print adc.read()
	except IoTPy_APIError, e: # don't see the UPER board
		details = e.args[0]
		die(details)


def call_back2():
	print "From call_back2..."
	try:
		green.write(0)
		sleep(0.2)
		green.write(1)
		print adc.read()
	except IoTPy_APIError, e: # don't see the UPER board
		details = e.args[0]
		die(details)


try:
	u = IoBoard()
except IoTPy_APIError, e: # seems can't establish connection with the UPER board
	details = e.args[0]
	die(details)

red = u.get_pin(GPIO, 27)
green = u.get_pin(GPIO, 28)
adc = u.get_pin(ADC, 23)


with u.get_pin(Interrupt, 40) as i1:
	i1.attach(Interrupt.EDGE_FALL, call_back1)
	print "Attached, detaching now on Interrupt object cleanup..."

i1 = u.get_pin(Interrupt, 40)
i1.attach(Interrupt.EDGE_CHANGE, call_back1)
i1.detach()

i1 = u.get_pin(Interrupt, 40)
i1.attach(Interrupt.EDGE_RISE, call_back1)

i2 = u.get_pin(Interrupt, 1)
i2.attach(Interrupt.EDGE_CHANGE, call_back2)

try:
	for i in range(60):
		u.get_device_info()
		sleep(1)
except IoTPy_APIError, e: # don't see the UPER board
	details = e.args[0]
	die(details)
except KeyboardInterrupt:
	errmsg("CTRL/C pressed, exiting.")
	exit(1)


