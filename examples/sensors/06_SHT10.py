from time import sleep

from IoTPy.boards.metis import Metis
from IoTPy.things.sht1x import SHT1X

with Metis() as board, board.digital("D3") as data_pin, board.digital("D2") as clock_pin, \
        SHT1X(data_pin, clock_pin) as sensor:
    while True:
        print("Temperature: %.1f Humidity: %.1f" % (sensor.temperature(), sensor.humidity()))
        sleep(1)
