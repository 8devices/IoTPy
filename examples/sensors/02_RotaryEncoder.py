from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.things.rotary_encoder import RotaryEncoder
from time import sleep


def on_rotation(direction, position):
    print "Rotated by %i, current position is %i" % (direction, position)


with IoBoard() as uper, \
        uper.GPIO(1) as chan0, uper.GPIO(2) as chan1, \
        RotaryEncoder(chan0, chan1, on_rotation) as encoder:
    while True:
        sleep(0.5)
