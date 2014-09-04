from IoTPy.core.gpio import GPIO
from IoTPy.pyuper.uper import UPER1

with UPER1() as board, board.GPIO(27) as redPin, board.GPIO(18) as buttonPin:

    buttonPin.setup(GPIO.INPUT, GPIO.PULL_UP)
    redPin.setup(GPIO.OUTPUT)

    oldState = buttonPin.read()
    redPin.write(oldState)

    nButtonPress = 0
    nButtonRelease = 0

    # This might look complicated, but all of the code in the while loop
    # can be replaced with redPin.write(buttonPin.read())
    # Variables and counters are here just for the print messages.
    while True:
        newState = buttonPin.read()

        if oldState != newState:
            oldState = newState

            if newState == 0:
                nButtonPress += 1
                print "Button pressed %i" % nButtonPress
                redPin.write(0)  # Turn led ON
            else:
                nButtonRelease += 1
                print "Button released %i" % nButtonRelease
                redPin.write(1)  # Turn led OFF