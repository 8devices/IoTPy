from IoTPy.interfaces.gpio import GPIO
from IoTPy.boards.metis import LPCexpresso

with LPCexpresso() as board, board.digital('P0_7') as redPin, board.digital('P0_23') as buttonPin:

    buttonPin.setup(GPIO.INPUT, GPIO.PULL_UP)
    redPin.setup(GPIO.OUTPUT)

    try:
        while True:
            redPin.write(buttonPin.read())
    except KeyboardInterrupt:
        pass