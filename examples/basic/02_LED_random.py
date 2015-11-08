import random
from time import sleep

from IoTPy.interfaces.gpio import GPIO

from IoTPy.boards.uper import UPER1

with UPER1() as board, \
        board.digital(27) as redPin, board.digital(28) as greenPin, board.digital(34) as bluePin:

    pins = [redPin, greenPin, bluePin]

    for pin in pins:
        pin.setup(GPIO.OUTPUT)  # set GPIO pins to be output

    while True:
        pin = random.choice(pins)  # choose random rgb pin
        pin.write(random.choice([0, 1]))  # randomly turn that pin on or off
        sleep(0.2)