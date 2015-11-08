from time import sleep

from IoTPy.ioboard.boards.uper import UPER1
from IoTPy.things.led_strip import LedStrip


def shift(seq, n):
    n %= len(seq)
    return seq[n:] + seq[:n]

with UPER1() as board, board.spi("SPI0", clock=2.9e6) as spi, LedStrip(spi) as leds:
    colors = [0xFF0000, 0xFFFF00, 0x00FF00, 0x0000FF, 0xFF00FF]
    while True:
        leds.set_colors(colors*10)
        colors = shift(colors, 1)
        sleep(0.2)
