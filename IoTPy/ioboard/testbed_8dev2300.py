from IoTPy.ioboard.ioboard import IoBoard
from IoTPy.ioboard.pinmaps import *

_8dev2300_PINOUT = IoPinout({
    'DUT_RESET':    P1_16,
    'DUT_POWER_EN': P0_7,
    'DUT_DETECT':   P0_22,
    'SWITCH1':      P0_15,
    'SWITCH2':      P0_17,
    'A_CURRENT':    P0_16,
    'BUZZER':       P1_15,
    'USB_POWER_EN': P1_19,
    'LED_R':        P1_25,
    'LED_G':        P1_26,
    'LED_B':        P1_24,
})

class _8dev2300(IoBoard):

    def __init__(self, serial_port=None):
        IoBoard.__init__(self, _8dev2300_PINOUT, serial_port)
