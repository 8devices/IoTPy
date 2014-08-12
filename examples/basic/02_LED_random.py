import random
from time import sleep
from IoTPy.core.gpio import GPIO
from IoTPy.pyuper.ioboard import IoBoard

with IoBoard() as uper, \
        uper.GPIO(27) as redPin, uper.GPIO(28) as greenPin, uper.GPIO(34) as bluePin:

    pins = [redPin, greenPin, bluePin]

    for pin in pins:
        pin.setup(GPIO.OUTPUT)  # set GPIO pins to be output

    while True:
        pin = random.choice(pins)  # choose random rgb pin
        pin.write(random.choice([0, 1]))  # randomly turn that pin on or off
        sleep(0.2)