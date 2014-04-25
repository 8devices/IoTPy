from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.adc import ADC
from IoTPy.pyuper.utils import IoTPy_APIError, die

"""
Read ADC value from pin No. 23 on UPER1 board
"""

try:
    with IoBoard() as board, board.get_pin(ADC, 23) as adc_pin:
        print "RAW ADC value:", adc_pin.read()
except IoTPy_APIError, e:  # seems can't establish connection with the board
    details = e.args[0]
    die(details)