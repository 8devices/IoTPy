from time import sleep
from IoTPy.pyuper.gpio import GPIO
from IoTPy.pyuper.interrupt import Interrupt
from IoTPy.pyuper.ioboard import IoBoard


def button_callback(event, obj):
    obj['counter'] += 1
    print "Interrupt %i" % obj['counter']

    button_state = (event['values'] >> event['id']) & 0x1
    obj['led'].write(button_state)

with IoBoard() as uper, GPIO(uper, 27) as redPin, Interrupt(uper, 18) as buttonPin:

    my_object = {'led': redPin, 'counter': 0}
    buttonPin.attach(Interrupt.EDGE_CHANGE, button_callback, my_object)
    redPin.mode(GPIO.OUTPUT)

    while True:
        sleep(0.5)