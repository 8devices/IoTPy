from IoTPy.interfaces.gpio import GPIO
from IoTPy.boards.metis import Metis
from time import sleep

with Metis() as board, board.digital('D16') as redPin, board.digital('D18') as buttonPin:

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
                print("Button pressed %i" % nButtonPress)
                redPin.write(0)  # Turn led ON
            else:
                nButtonRelease += 1
                print("Button released %i" % nButtonRelease)
                redPin.write(1)  # Turn led OFF
        #sleep(0.93)
