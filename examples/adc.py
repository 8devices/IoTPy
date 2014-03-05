from pyuper.uperio import UperIO
from pyuper.adc import ADC
from time import sleep
from pyuper.utils import UPER_APIError, die

try:
	u = UperIO()
except UPER_APIError, e: # seems can't establish connection with the UPER board
	details = e.args[0]
	die(details)

try: # let's try to attach ADC object to non ADC pin
	a = u.get_pin(ADC, 27)
except UPER_APIError, e: # got an exception, pin capabilities must be different from requested
	details = e.args[0]
	print details

with u.get_pin(ADC, 23) as adc_pin:
	for i in range(10):
		val = adc_pin.read()
		print "RAW ADC value:", val
		voltage = 5.0/1024 * val
		print voltage, "V"
		if val > 2:
			# printing distance from sensor hopefully in cm.
			print (6787/(val-3))-4, "cm"
		sleep(0.5)