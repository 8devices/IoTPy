from IoTPy.ioboard.ioboard import IoBoard
from IoTPy.ioboard.pinmaps import *

LPCExpresso11U14REVA_PINOUT = IoPinout({
    1: P_GND,
    2: P_5V,
    3: P_GND,
    4: P_GND,
    'P0_9':     P0_9,
    'P0_8':     P0_8,
    'P1_29':    P1_29,
    'P0_2':     P0_2,
    'P0_19':    P0_19,
    'P0_18':    P0_18,
    'P0_7':     P0_7,
    'P1_21':    P1_21,
    'P0_11':    P0_11,
    'P0_12':    P0_12,
    'P0_13':    P0_13,
    'P0_14':    P0_14,
    'P0_15':    P0_15,
    'P0_16':    P0_16,
    'P0_17':    P0_17,
    'P0_20':    P0_20,
    'P0_10':    P0_10,
    'P1_13':    P1_13,
    'P1_14':    P1_14,
    'P1_15':    P1_15,
    'P0_21':    P0_21,
    'P0_22':    P0_22,
    'P0_23':    P0_23,
    'P1_22':    P1_22,
    'P1_23':    P1_23,
    'P1_24':    P1_24,
    'P1_25':    P1_25,
    'P1_26':    P1_26,
    'P1_27':    P1_27,
    'P1_31':    P1_31,
    'P1_16':    P1_16,
})


class VirtualSFP(IoBoard):

    def __init__(self, transport):
        IoBoard.__init__(self, LPCExpresso11U14REVA_PINOUT, transport )
