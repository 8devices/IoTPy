from time import sleep
from IoTPy.ioboard.uper import UPER1
from IoTPy.things.sht1x import SHT1X

with UPER1 as board, board.GPIO(1) as data, board.GPIO(2) as sck, SHT1X(data, sck) as sensor:
    while True:
        print "Temperature: %.1f Humidity: %.1f" % (sensor.temperature(), sensor.humidity())
        sleep(1)
