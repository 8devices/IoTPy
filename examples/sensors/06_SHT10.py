from time import sleep
from IoTPy.pyuper.gpio import GPIO
from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.things.sht1x import SHT1X

with IoBoard() as uper, GPIO(uper, 2) as data, GPIO(uper, 1) as sck, SHT1X(data, sck) as sensor:
    while True:
        print "Temperature: %.1f Humidity: %.1f" % (sensor.temperature(), sensor.humidity())
        sleep(1)