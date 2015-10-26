from IoTPy.core.gpio import GPIO
from IoTPy.ioboard.lpcexpresso11u14 import LPCexpresso

with LPCexpresso() as board, board.GPIO('P0_7') as redPin, board.GPIO('P0_23') as buttonPin:

    buttonPin.setup(GPIO.INPUT, GPIO.PULL_UP)
    redPin.setup(GPIO.OUTPUT)

    try:
        while True:
            redPin.write(buttonPin.read())
    except KeyboardInterrupt:
        pass