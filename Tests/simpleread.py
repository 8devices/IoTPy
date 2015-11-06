from IoTPy.core.gpio import GPIO
from IoTPy.ioboard.lpcexpresso11u14 import LPCexpresso

with LPCexpresso() as board, board.GPIO('P0_23') as pin:
#    pin.setup(GPIO.INPUT)
    print(pin.read())
    print(pin.read())
    print(pin.read())

    print(board.get_device_info())