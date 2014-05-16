from time import time
from datetime import datetime
from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.interrupt import Interrupt
from IoTPy.pyuper.utils import IoTPy_APIError, die, errmsg
from IoTPy.pyuper.gpio import GPIO
a = 0
previous_time = 0

try:
    u = IoBoard()
except IoTPy_APIError, e:
    details = e.args[0]
    die(details)

def call_back2():
    global a
    global previous_time
    C=PINa.read()
    time_now = time() * 1000
    #print time_now - previous_time
    if time_now - previous_time > 200:
        if C:
            a += 1
        else:
            a -= 1
        print a,"C=",C
    #else:
        #print "skipping"
    previous_time = time_now

PINb = u.get_pin(GPIO, 1)
PINb.mode(GPIO.PULL_UP)
PINa = u.get_pin(GPIO, 2)
PINa.mode(GPIO.PULL_UP)

i2 = u.get_pin(Interrupt, 1)
i2.attach(Interrupt.EDGE_RISE, call_back2)



print "program started"

while True :
	pass
