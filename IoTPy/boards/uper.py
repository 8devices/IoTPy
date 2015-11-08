from IoTPy.ioboard.ioboard import IoBoard
from IoTPy.ioboard.pinmaps import *

UPER1_PINOUT = IoPinout({
    1: P0_20,
    2: P0_2,
    3: P1_26,
    4: P1_27,
    5: P1_20,
    6: P_I2C,
    7: P_I2C,
    8: P0_21,
    9: P1_23,
    10:P1_24,
    11:P0_7,
    12:P1_28,
    13:P1_31,
    14:P1_21,
    15:P0_8,
    16:P0_9,
    17:P0_10,
    18:P1_29,
    19:P_5V,
    20:P_GND,
    21:P_GND,
    22:P_3V,
    23:P0_11,
    24:P0_12,
    25:P0_13,
    26:P0_14,
    27:P1_13,
    28:P1_14,
    29:P1_22,
    30:P0_15,
    31:P0_16,
    32:P0_22,
    33:P0_23,
    34:P1_15,
    35:P0_17,
    36:P0_18,
    37:P0_19,
    38:P0_16,
    39:P1_25,
    40:P1_19
})

class UPER1(IoBoard):

    def __init__(self, io=None):
        IoBoard.__init__(self, UPER1_PINOUT, io)
