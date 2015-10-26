from time import sleep
from IoTPy.core.gpio import GPIO
from IoTPy.ioboard.lpcexpresso11u14 import LPCexpresso

# This is platform dependent - please configure to your application
LED_PIN_ID = 'P0_7'

with LPCexpresso() as board, board.GPIO(LED_PIN_ID) as ledPin:
    ledPin.setup(GPIO.OUTPUT)  # set GPIO pin to be output
    try:
        while True:
            ledPin.write(1)  # Turn led ON
            sleep(0.2)
            ledPin.write(0)  # Turn led OFF
            sleep(0.2)
    except KeyboardInterrupt:
        ledPin.write(0)  # Turn led OFF
        pass