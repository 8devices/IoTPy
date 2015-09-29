from time import sleep
from IoTPy.core.gpio import GPIO

_UPER1 = 1
_LPCexpresso = 2

ioBoardType = _LPCexpresso

if ioBoardType == _UPER1:
    from IoTPy.ioboard.uper import UPER1 as ioBoard
    LED_PIN_ID = 27
if ioBoardType == _LPCexpresso:
    from IoTPy.ioboard.lpcexpresso11u14 import LPCexpresso as ioBoard
    LED_PIN_ID = 'P0_7'

# This is platform dependent - please configure to your application

with ioBoard() as board, board.GPIO(LED_PIN_ID) as ledPin:

    ledPin.setup(GPIO.OUTPUT)  # set GPIO pin to be output

    while True:
        ledPin.write(0)  # Turn led ON (LED on board is common anode - therefore inverted)
        sleep(0.5)
        ledPin.write(1)  # Turn led OFF
        sleep(0.5)