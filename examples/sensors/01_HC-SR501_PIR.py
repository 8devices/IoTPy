from time import sleep
from IoTPy.pyuper.gpio import GPIO
from IoTPy.pyuper.interrupt import Interrupt
from IoTPy.pyuper.ioboard import IoBoard


def pir_callback(event, obj):
    print event
    if event['type'] == Interrupt.EDGE_RISE:
        print "Movement detected"
        obj['led'].write(0)  # turn ON the led
    elif event['type'] == Interrupt.EDGE_FALL:
        print "No movement"
        obj['led'].write(1)  # turn OFF the led
    else:
        print "Unknown event"

with IoBoard() as uper, GPIO(uper, 27) as redPin, Interrupt(uper, 18) as buttonPin:

    my_object = {'led': redPin}
    buttonPin.attach(Interrupt.EDGE_CHANGE, pir_callback, my_object)
    redPin.mode(GPIO.OUTPUT)

    while True:
        sleep(0.5)
