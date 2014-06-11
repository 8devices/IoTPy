from time import sleep
from IoTPy.pyuper.gpio import GPIO
from IoTPy.pyuper.ioboard import IoBoard

with IoBoard() as uper, GPIO(uper, 27) as redPin:

    redPin.mode(GPIO.OUTPUT)  # set GPIO pin to be output

    while True:
        redPin.write(0)  # Turn led ON (LED on board is common anode - therefore inverted)
        sleep(0.5)
        redPin.write(1)  # Turn led OFF
        sleep(0.5)