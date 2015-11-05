from IoTPy.ioboard.ioboard import IoBoard
from IoTPy.ioboard.pinmaps import *

WEIO_PINOUT = IoPinout({
    0: P0_18,
    1: P0_19,
    2: P0_9,
    3: P0_8,
    4: P0_10,
    5: P0_2,
    6: P0_7,
    7: P0_17,
    8: P0_20,
    9: P1_16,
    10:P0_21,
    11:P1_21,
    12:P1_20,
    13:P1_19,
    14:P1_22,
    15:P1_23,
    16:P1_27,
    17:P1_28,
    18:P1_13,
    19:P1_14,
    20:P1_15,
    21:P1_24,
    22:P1_25,
    23:P1_26,
    24:P0_11,
    25:P0_12,
    26:P0_13,
    27:P0_14,
    28:P0_15,
    29:P0_16,
    30:P0_22,
    31:P0_23
})

class WeIO(IoBoard):

    def __init__(self, serial_port=None):
        IoBoard.__init__(self, WEIO_PINOUT, serial_port)
