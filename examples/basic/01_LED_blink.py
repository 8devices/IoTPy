from time import sleep
from IoTPy.core.gpio import GPIO
from IoTPy.pyuper.uper import UPER1

# This is platform dependent - please configure to your application
LED_PIN_ID = 27

with UPER1() as board, board.GPIO(LED_PIN_ID) as redPin:

    redPin.setup(GPIO.OUTPUT)  # set GPIO pin to be output

    while True:
        redPin.write(0)  # Turn led ON (LED on board is common anode - therefore inverted)
        sleep(0.5)
        redPin.write(1)  # Turn led OFF
        sleep(0.5)