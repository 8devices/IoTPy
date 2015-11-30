from time import sleep
from IoTPy.interfaces.gpio import GPIO

_UPER1 = 1
_LPCexpresso = 2

ioBoardType = _LPCexpresso

if ioBoardType == _UPER1:
    from IoTPy.boards.uper import UPER1 as ioBoard
    LED_PIN_ID = 27
if ioBoardType == _LPCexpresso:
    from IoTPy.boards.metis import LPCexpresso as ioBoard
    LED_PIN_ID = 'P0_7'

# This is platform dependent - please configure to your application

with ioBoard() as board, board.digital(LED_PIN_ID) as ledPin:

    ledPin.setup(GPIO.OUTPUT)  # set GPIO pin to be output

    while True:
        ledPin.write(0)  # Turn led ON (LED on board is common anode - therefore inverted)
        sleep(0.5)
        ledPin.write(1)  # Turn led OFF
        sleep(0.5)