from time import sleep

from IoTPy.ioboard.boards.uper import UPER1
from IoTPy.things.rotary_encoder import RotaryEncoder


def on_rotation(direction, position):
    print("Rotated by %i, current position is %i" % (direction, position))


with UPER1() as board, \
        board.digital(1) as chan0, board.digital(2) as chan1, \
        RotaryEncoder(chan0, chan1, on_rotation) as encoder:

    while True:
        sleep(0.5)
