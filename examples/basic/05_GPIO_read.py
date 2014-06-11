from IoTPy.pyuper.gpio import GPIO
from IoTPy.pyuper.ioboard import IoBoard

with IoBoard() as uper, GPIO(uper, 27) as redPin, GPIO(uper, 18) as buttonPin:

    buttonPin.mode(GPIO.PULL_UP)
    redPin.mode(GPIO.OUTPUT)

    oldState = buttonPin.read()
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