from time import sleep

from IoTPy.boards.metis import Metis
from IoTPy.things.si70xx import Si7013, Si7020

#with Metis() as board, board.i2c("I2C0") as i2c, Si7020(i2c, 0x40) as si7020, Si7013(i2c, 0x41) as si7013:
with Metis() as board, board.i2c("I2C0") as i2c, Si7013(i2c, 0x40) as si7013:
    while True:
        #print("Si7020 T=%.1f H=%.1f" % (si7020.temperature(), si7020.humidity()))
        print("Si7013 T=%.1f H=%.1f A=%i" % (si7013.temperature(), si7013.humidity(), si7013.analog()))
        sleep(1)