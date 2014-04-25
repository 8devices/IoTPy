from itertools import cycle
from time import sleep

from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.gpio import GPIO
from IoTPy.pyuper.utils import IoTPy_APIError, die

try:
    u = IoBoard()
except IoTPy_APIError, e: # seems can't establish connection with the UPER board
    details = e.args[0]
    die(details)

try:  # set GPIO on ground pin
    a = u.get_pin(GPIO, 20)
except IoTPy_APIError, e:
    details = e.args[0]
    print details

with u.get_pin(GPIO, 27) as r, u.get_pin(GPIO, 28) as g, u.get_pin(GPIO, 34) as b:
    b.mode(GPIO.PULL_DOWN)
    print b.read()
    b.mode(GPIO.PULL_UP)
    print b.read()
    try:
        for i in cycle([0,1]):
            r.write(i)
            g.write(i)
            b.write(i)
            sleep(0.5)
    except KeyboardInterrupt:
        die("Keyboard interrupt.")