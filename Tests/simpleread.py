from IoTPy.boards.lpcexpresso11u14 import LPCexpresso
from IoTPy.transport import SocketTransport

with LPCexpresso(SocketTransport()) as board, board.digital('P0_23') as pin:
#    pin.setup(GPIO.INPUT)
    print(pin.read())
    print(pin.read())
    print(pin.read())

    print(board.get_device_info())