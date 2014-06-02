from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.interrupt import Interrupt
from IoTPy.pyuper.utils import IoTPy_APIError, IoTPy_IOError, die
from IoTPy.pyuper.gpio import GPIO

from time import sleep

backwardStates = [
    [[0, 0], [1, 0], [1, 1]], # missing 1st
    [[0, 1], [1, 0], [1, 1]], # missing 2nd
    [[0, 1], [0, 0], [1, 1]], # missing 3rd
    [[0, 1], [0, 0], [1, 0]], # missing 4th
]

forwardStates  = [
    [[0, 0], [0, 1], [1, 1]], # missing 1st or perfect
    [[1, 0], [0, 1], [1, 1]], # missing 2nd
    [[1, 0], [0, 0], [1, 1]], # missing 3rd
    [[1, 0], [0, 0], [0, 1]], # missing 4th
]

nullState = [ [-1, -1], [-1, -1], [-1, -1] ]

global lastStates
global position

lastStates =  list(nullState)
position = 0

def call_back(args):
    global lastStates
    global position

    try:
        pins = args[1] >> 8
        thisA = pins & 0x01
        thisB = (pins >> 1) & 0x01
        
        if [thisA, thisB] != lastStates[2]:
            lastStates[0:2] = lastStates[1:3]
            lastStates[2] = [thisA, thisB]

            #print thisA, thisB

            if lastStates in forwardStates:
                position = position + 1
                print "Forward: %i" % position
                lastStates = list(nullState)
            elif lastStates in backwardStates:
                position = position - 1
                print "Backward %i" % position
                lastStates = list(nullState)
    except:
        print "Callback Exception"

try:
    with IoBoard() as u:
        u.get_pin(GPIO, 1).mode(GPIO.PULL_UP)
        u.get_pin(GPIO, 2).mode(GPIO.PULL_UP)
        u.get_pin(Interrupt, 1).attach(Interrupt.EDGE_CHANGE, call_back, 1)
        u.get_pin(Interrupt, 2).attach(Interrupt.EDGE_CHANGE, call_back, 1)

        while True:
            sleep(0.5)
except KeyboardInterrupt:
    print "CTRL/C pressed, exiting."
    exit(0)
except (IoTPy_IOError, IoTPy_APIError), e: # don't see the I2C bus or UPER board
    details = e.args[0]
    die(details)