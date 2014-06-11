import random
from time import sleep
from IoTPy.pyuper.gpio import GPIO
from IoTPy.pyuper.ioboard import IoBoard

with IoBoard() as uper, GPIO(uper, 27) as redPin, GPIO(uper, 28) as greenPin, \
        GPIO(uper, 34) as bluePin:

    pins = [redPin, greenPin, bluePin]

    for pin in pins:
        pin.mode(GPIO.OUTPUT)  # set GPIO pins to be output

    while True:
        pin = random.choice(pins)  # choose random rgb pin
        pin.write(random.choice([0, 1]))  # randomly turn that pin on or off
        sleep(0.2)