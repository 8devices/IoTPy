from IoTPy.boards.metis import Metis
from time import sleep

with Metis() as board, board.analog("D11") as adcPin1, board.pwm("D4") as pwmPin:
    pwmPin.set_frequency(1000)
    while True:
        for i in xrange(0, 100):
            pwmPin.set_duty_cycle(i)
            sleep(0.01)
        for i in reversed(xrange(0, 100)):
            pwmPin.set_duty_cycle(i)
            sleep(0.01)
        print(adcPin1.read())
        sleep(0.1)
