__author__ = 'jonas'
from IoTPy.ioboard.utils import IoTPy_APIError
import collections
from six import string_types

# thanks to Mark Lodato for nice structure published on stackoverflow!
def namedtuple_with_defaults(typename, field_names, default_values=[]):
    T = collections.namedtuple(typename, field_names)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    if isinstance(default_values, collections.Mapping):
        prototype = T(**default_values)
    else:
        prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T

CAP_RESERVED = 0x0
CAP_GPIO     = 0x1
CAP_ADC      = 0x2
CAP_PWM      = 0x4
CAP_SPI      = 0x8
CAP_UART     = 0x10

"""
named tuple Pin for storing pinID, capabilities and extra info such us PWN bank or ADS pin no and similar.
"""
Pin = namedtuple_with_defaults('Pin','pinID, capabilities, extra', [None, CAP_GPIO, None])

class IoPinout(dict):
    """
    A dictionary consisting of integer or basestring keys and named tuple Pin
    """
    def __init__(self, *args, **kw):
        super(IoPinout,self).__init__(*args, **kw)
        for key in self:
            if not (isinstance(key, int) or isinstance(key, string_types)) or not isinstance(self[key], Pin):
                raise IoTPy_APIError("IoPinout must consist of integer or string keys and Pin values.")

    def __delitem__(self, key):
        raise IoTPy_APIError("IoPinout can not be modified.")

    def __setitem__(self, key, value):
        raise IoTPy_APIError("IoPinout can not be modified.")

P0_20   = Pin(0)
P0_2    = Pin(1)
P1_26   = Pin(2, CAP_GPIO | CAP_PWM, [1,2]) #PWM1_2
P1_27   = Pin(3)
P1_20   = Pin(4, CAP_GPIO | CAP_SPI, [1,2]) #SPI1 SCK
P0_21   = Pin(5, CAP_GPIO | CAP_SPI, [1,1]) #SPI1 MOSI
P1_23   = Pin(6)
P1_24   = Pin(7, CAP_GPIO | CAP_PWM, [1,0]) #PWM1_0
P0_7    = Pin(8)
P1_28   = Pin(9)
P1_31   = Pin(10)
P1_21   = Pin(11, CAP_GPIO | CAP_SPI, [1,0]) #SPI1 MISO
P0_8    = Pin(12, CAP_GPIO | CAP_SPI, [0,0]) #SPI0 MISO
P0_9    = Pin(13, CAP_GPIO | CAP_SPI, [0,1]) #SPI0 MOSI
P0_10   = Pin(14, CAP_GPIO | CAP_SPI, [0,2]) #SPI0 SCK
P1_29   = Pin(15)
P1_19   = Pin(16)
P1_25   = Pin(17, CAP_GPIO | CAP_PWM, [1,1]) #PWM1_1
P1_16   = Pin(18)
P0_19   = Pin(19, CAP_GPIO | CAP_UART, [0])  #UART TX
P0_18   = Pin(20, CAP_GPIO | CAP_UART, [1])  #UART RX
P0_17   = Pin(21)
P1_15   = Pin(22, CAP_GPIO | CAP_PWM, [0,2]) #PWM0_2
P0_23   = Pin(23, CAP_GPIO | CAP_ADC, [7])   #ADC7
P0_22   = Pin(24, CAP_GPIO | CAP_ADC, [6])   #ADC6
P0_16   = Pin(25, CAP_GPIO | CAP_ADC, [5])   #ADC5
P0_15   = Pin(26, CAP_GPIO | CAP_ADC, [4])   #ADC4
P1_22   = Pin(27)
P1_14   = Pin(28, CAP_GPIO | CAP_PWM, [0,1]) #PWM0_1
P1_13   = Pin(29, CAP_GPIO | CAP_PWM, [0,0]) #PWM0_0
P0_14   = Pin(30, CAP_GPIO | CAP_ADC, [3])   #ADC3
P0_13   = Pin(31, CAP_GPIO | CAP_ADC, [2])   #ADC2
P0_12   = Pin(32, CAP_GPIO | CAP_ADC, [1])   #ADC1
P0_11   = Pin(33, CAP_GPIO | CAP_ADC, [2])   #ADC0

P_GND   = Pin(-1, CAP_RESERVED)
P_5V    = Pin(-1, CAP_RESERVED)
P_3V    = Pin(-1, CAP_RESERVED)
P_I2C   = Pin(-1, CAP_RESERVED)
P_DONO  = Pin(-1, CAP_RESERVED)

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

_8dev2300_PINOUT = IoPinout({
    'DUT_RESET':    P1_16,
    'DUT_POWER_EN': P0_7,
    'SWITCH1':      P0_15,
    'SWITCH2':      P0_17,
    'A_CURRENT':    P0_16,
    'BUZZER':       P1_15,
    'USB_POWER_EN': P1_19,
    'LED_R':        P1_25,
    'LED_G':        P1_26,
    'LED_B':        P1_24,
})


