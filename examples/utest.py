from IoTPy.pyuper.ioboard import IoBoard
from time import sleep

i = 0

while True:
    u = IoBoard()
    #info = u.get_device_info()
    i += 1
    if not (i % 1):
        print i
    u.stop()
    #sleep(0.3)while True:
"""
with IoBoard() as u:
        info = u.get_device_info()
        i += 1
        if not (i % 10):
            print i
    #sleep(0.3)


with IoBoard() as u:
    while True:
        info = u.get_device_info()
        i += 1
        if not (i % 10):
            print i
        #sleep(0.1)
"""