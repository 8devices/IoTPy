from time import sleep
from IoTPy.core.gpio import GPIO
from IoTPy.ioboard.uper import UPER1


def button_callback(event, obj):
    obj['counter'] += 1
    print "Interrupt %i" % obj['counter']

    button_state = (event['values'] >> event['id']) & 0x1
    obj['led'].write(button_state)

with UPER1() as board, board.GPIO(27) as redPin, board.GPIO(18) as buttonPin:

    my_object = {'led': redPin, 'counter': 0}
    buttonPin.attach_irq(GPIO.CHANGE, button_callback, my_object)

    redPin.setup(GPIO.OUTPUT)
    redPin.write(1)

    while True:
        sleep(0.5)