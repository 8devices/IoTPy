from time import sleep
from IoTPy.ioboard.uper import UPER1
from IoTPy.things.am2321 import AM2321

with UPER1() as board, board.I2C("I2C0") as i2c, AM2321(i2c) as sensor:
    while True:
        sensor.read()
        print("Temperature: %.1f Humidity: %.1f" % (sensor.temperature, sensor.humidity))
        sleep(1)