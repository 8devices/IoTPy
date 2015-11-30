from IoTPy.ioboard import IoBoard
from IoTPy.pinmaps import *

METIS_PINOUT = IoPinout({

    'D0':   P0_4,    # I2C
    'D1':   P0_5,    # I2C
    'D2':   P1_19,
    'D3':   P0_21,
    'D4':   P1_15,
    'D5':   P0_22,
    'D6':   P0_8,
    'D7':   P0_9,
    'D8':   P0_10,
    'D9':   P0_11,
    'D10':  P0_12,
    'D11':  P0_13,
    'D12':  P0_14,
    'D13':  P0_16,
    'D14':  P0_23,
    'D15':  P0_15,
    'D16':  P0_7,     # blue LED
    'D17':  P0_17,
    'D18':  P0_1,     # Program button
    'D19':  P0_19,
    'D20':  P0_18,
    'D21':  P0_20,
    'D22':  P0_2,
})


class Metis(IoBoard):

    def __init__(self, io=None):
        IoBoard.__init__(self, METIS_PINOUT, io)
