import signal
from time import sleep
from IoTPy.interfaces.gpio import GPIO
from IoTPy.boards.metis import Metis
from IoTPy.transport import SocketTransport, SerialTransport


def button_callback(event, obj):
    obj['counter'] += 1
    print("Interrupt %i" % obj['counter'])

    button_state = (event['values'] >> event['id']) & 0x1
    obj['led'].write(button_state)

io = SerialTransport()
with Metis(io) as board, board.digital('D16') as led, board.digital('D18') as button_pin:
    my_object = {'led': led, 'counter': 0}
    button_pin.attach_irq(GPIO.CHANGE, button_callback, my_object)
    led.write(1)

    try:
        signal.pause()
    except AttributeError:
        # signal.pause() is missing for Windows, loop instead
        while True:
            sleep(1)
