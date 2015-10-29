from colorsys import hls_to_rgb
from time import sleep
from IoTPy.ioboard.lpcexpresso11u14 import LPCexpresso as ioBoard

with ioBoard() as board, \
        board.PWM('P1_25', polarity=0) as redPin, board.PWM('P1_26', polarity=0) as greenPin, \
        board.PWM('P1_24', polarity=0) as bluePin, board.PWM('P1_15', polarity=0) as buzzerPin:

    buzzerPin.set_frequency(440)
    buzzerPin.set_duty_cycle(70)
    while True:
        for color in xrange(500):
            rgb = hls_to_rgb(color*0.002, 0.1, 1)
            redPin.set_duty_cycle(rgb[0]*100)
            greenPin.set_duty_cycle(rgb[1]*100)
            bluePin.set_duty_cycle(rgb[2]*100)
            sleep(0.002)