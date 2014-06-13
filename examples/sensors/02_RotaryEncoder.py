from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.interrupt import Interrupt
from IoTPy.pyuper.gpio import GPIO

from time import sleep

backwardStates = [
    [[0, 0], [1, 0], [1, 1]],  # missing 1st
    [[0, 1], [1, 0], [1, 1]],  # missing 2nd
    [[0, 1], [0, 0], [1, 1]],  # missing 3rd
    [[0, 1], [0, 0], [1, 0]],  # missing 4th
]

forwardStates = [
    [[0, 0], [0, 1], [1, 1]],  # missing 1st or perfect
    [[1, 0], [0, 1], [1, 1]],  # missing 2nd
    [[1, 0], [0, 0], [1, 1]],  # missing 3rd
    [[1, 0], [0, 0], [0, 1]],  # missing 4th
]

nullState = [[-1, -1], [-1, -1], [-1, -1]]


def call_back(event, obj):
    previous_states = obj['previous_states']
    position = obj['position']

    pins = event['values']
    pin1 = (pins >> 0) & 0x01
    pin2 = (pins >> 1) & 0x01
    
    if [pin1, pin2] != previous_states[2]:
        previous_states[0:2] = previous_states[1:3]
        previous_states[2] = [pin1, pin2]

        #print pin1, pin2

        if previous_states in forwardStates:
            position += 1
            print "Forward: %i" % position
            previous_states = list(nullState)
        elif previous_states in backwardStates:
            position -= 1
            print "Backward %i" % position
            previous_states = list(nullState)

    obj['previous_states'] = previous_states
    obj['position'] = position

with IoBoard() as uper:
    
    user_obj = {'previous_states': list(nullState), 'position': 0}
    
    uper.get_pin(GPIO, 1).mode(GPIO.PULL_UP)
    uper.get_pin(GPIO, 2).mode(GPIO.PULL_UP)
    uper.get_pin(Interrupt, 1).attach(Interrupt.EDGE_CHANGE, call_back, user_obj, 3)
    uper.get_pin(Interrupt, 2).attach(Interrupt.EDGE_CHANGE, call_back, user_obj, 3)

    while True:
        sleep(0.5)
