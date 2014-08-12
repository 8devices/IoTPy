from time import sleep
from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.things.lm75 import Lm75

with IoBoard() as uper, uper.I2C("I2C0") as i2c, Lm75(i2c, 79) as lm75:
    while True:
        print lm75.temperature()
        sleep(0.1)