from time import sleep
from IoTPy.interfaces.gpio import GPIO
from IoTPy.boards.lpcexpresso11u14 import LPCexpresso
from IoTPy.transport import SocketTransport


def button_callback(event, obj):
    obj['counter'] += 1
    print("Interrupt %i" % obj['counter'])

    button_state = (event['values'] >> event['id']) & 0x1
    obj['led'].write(button_state)

io = SocketTransport()
with LPCexpresso(io) as board, board.digital('P0_7') as redPin, board.digital('P0_23') as buttonPin:
    my_object = {'led': redPin, 'counter': 0}
    buttonPin.attach_irq(GPIO.CHANGE, button_callback, my_object)

    redPin.setup(GPIO.OUTPUT)
    redPin.write(1)
    while True:
        sleep(0.5)