from IoTPy.boards.lpcexpresso11u14 import LPCexpresso
from IoTPy.transport import SocketTransport
from IoTPy.interfaces.gpio import GPIO
from time import time

with LPCexpresso(SocketTransport()) as board, board.digital('P0_23') as pin:
    pin.setup(GPIO.INPUT)
    pin.write(1)
    print(pin.read())
    pin.write(0)
    print(pin.read())
    pin.write(1)
    start = time()
    for i in range(10000):
        pin.read()
    for i in range(10000):
        pin.write(1)
    end = time()
    print("elapsed time (s) %f" % (end - start))
    print(pin.read())
    print(board.get_device_info())
