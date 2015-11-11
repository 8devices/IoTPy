from IoTPy.boards.lpcexpresso11u14 import LPCexpresso
from IoTPy.transport import SocketTransport
from IoTPy.interfaces.gpio import GPIO

with LPCexpresso(SocketTransport()) as board, board.digital('P0_23') as pin:
    pin.setup(GPIO.INPUT)
    pin.write(1)
    print(pin.read())
    pin.write(0)
    print(pin.read())
    pin.write(1)
    print(pin.read())
    print(board.get_device_info())
