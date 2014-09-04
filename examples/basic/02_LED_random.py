import random
from time import sleep
from IoTPy.core.gpio import GPIO
from IoTPy.pyuper.uper import UPER1

with UPER1() as board, \
        board.GPIO(27) as redPin, board.GPIO(28) as greenPin, board.GPIO(34) as bluePin:

    pins = [redPin, greenPin, bluePin]

    for pin in pins:
        pin.setup(GPIO.OUTPUT)  # set GPIO pins to be output

    while True:
        pin = random.choice(pins)  # choose random rgb pin
        pin.write(random.choice([0, 1]))  # randomly turn that pin on or off
        sleep(0.2)