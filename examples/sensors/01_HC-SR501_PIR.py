from time import sleep
from IoTPy.core.gpio import GPIO
from IoTPy.pyuper.uper import UPER1


def pir_callback(event, obj):
    print event
    if event['type'] == GPIO.RISE:
        print "Movement detected"
        led.write(0)  # turn ON the led
    elif event['type'] == GPIO.FALL:
        print "No movement"
        led.write(1)  # turn OFF the led
    else:
        print "Unknown event"

with UPER1() as board, board.GPIO(27) as led, board.GPIO(18) as button:

    button.setup(GPIO.INPUT, GPIO.PULL_UP)
    button.attach_irq(GPIO.CHANGE, pir_callback, led)

    led.setup(GPIO.OUTPUT)
    led.write(1)

    while True:
        sleep(0.5)
