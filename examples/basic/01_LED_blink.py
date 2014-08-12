from time import sleep
from IoTPy.core.gpio import GPIO
from IoTPy.pyuper.ioboard import IoBoard

with IoBoard() as uper, uper.GPIO(27) as redPin:

    redPin.setup(GPIO.OUTPUT)  # set GPIO pin to be output

    while True:
        redPin.write(0)  # Turn led ON (LED on board is common anode - therefore inverted)
        sleep(0.5)
        redPin.write(1)  # Turn led OFF
        sleep(0.5)