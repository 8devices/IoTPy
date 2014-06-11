from time import sleep
from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.pwm import PWM

with IoBoard() as uper, PWM(uper, 27) as redPin:

    redPin.period(100)  # set PWM period to 100us

    while True:
        for i in xrange(0, 100):
            redPin.width_us(i)
            sleep(0.01)
        for i in reversed(xrange(0, 100)):
            redPin.width_us(i)
            sleep(0.01)