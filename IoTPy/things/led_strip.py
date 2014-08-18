

class LedStrip:

    def __init__(self, spi):
        self.spi = spi

        self.set_color(0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def set_colors(self, colors):
        data = "\x00\x00\x00\x00"

        for color in colors:
            r = color >> 19 & 0x1F
            g = color >> 11 & 0x1F
            b = color & 0x1F
            tmp = 0x8000 | (b << 10) | (r << 5) | g
            data += chr(tmp >> 8) + chr(tmp & 0xFF)

        for i in xrange((len(colors)+7)/8):
            data += '\x00'

        self.spi.write(data)

    def set_color(self, color):
        self.set_colors([color] * 50)