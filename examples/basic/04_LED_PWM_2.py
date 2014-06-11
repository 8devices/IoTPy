from colorsys import hls_to_rgb
from time import sleep
from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.pwm import PWM

with IoBoard() as uper, \
        PWM(uper, 27) as redPin, PWM(uper, 28) as greenPin, PWM(uper, 34) as bluePin:

    while True:
        for color in xrange(500):
            rgb = hls_to_rgb(color*0.002, 0.1, 1)
            redPin.write(rgb[0])
            greenPin.write(rgb[1])
            bluePin.write(rgb[2])
            sleep(0.002)