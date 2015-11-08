from colorsys import hls_to_rgb
from time import sleep

from IoTPy.boards.uper import UPER1

with UPER1() as board, \
        board.pwm(27, polarity=0) as redPin, board.pwm(28, polarity=0) as greenPin, board.pwm(34, polarity=0) as bluePin:

    while True:
        for color in xrange(500):
            rgb = hls_to_rgb(color*0.002, 0.1, 1)
            redPin.set_duty_cycle(rgb[0]*100)
            greenPin.set_duty_cycle(rgb[1]*100)
            bluePin.set_duty_cycle(rgb[2]*100)
            sleep(0.002)