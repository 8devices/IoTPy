from math import exp
from colorsys import hls_to_rgb
import random
import struct
import threading
from time import sleep


class Wire:

    def __init__(self, board, pin):
        self.board = board
        self.pin = pin

    def __enter__(self):
        self.board.uper_io(0, self.board.encode_sfp(100, [1]))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def trans(self, data):
        self.board.uper_io(0, self.board.encode_sfp(101, [data]))


class LedStrip:

    def __init__(self, wire, length):
        self.wire = wire
        self.n_leds = length

        self.set_color(0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @staticmethod
    def c2rgb(c):
        return (c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF

    @staticmethod
    def rgb2c(r, g, b):
        return ((int(r) & 0xFF) << 16) | ((int(g) & 0xFF) << 8) | (int(b) & 0xFF)

    def set_colors(self, colors):
        data = ""

        for c in colors:
            data += struct.pack("BBB", (c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF)

        self.wire.trans(data)

    def set_color(self, color):
        self.set_colors([color] * self.n_leds)

    def set_random_nice_colors(self):
        colors = [0, ] * self.n_leds
        for i in xrange(31, self.n_leds):
            r, g, b = hls_to_rgb(random.random(), 0.3, 1)
            colors[i] = (int(r*255) << 16 | int(g*255) << 8 | int(b*255))
        self.set_colors(colors)

    def start_composition(self):
        self.colors = [0]*self.n_leds

    def finish_composition(self):
        self.set_colors(self.colors)

    def add_peak(self, color, pos, width):
        self.colors[pos:pos+width] = [color]*width

    def add_gauss(self, color, pos, sigma):
        sigma = float(sigma)
        r, g, b = self.c2rgb(color)
        for x, col in enumerate(self.colors):
            gauss = exp(-0.5*((x-pos)/sigma)**2)
            r1, g1, b1 = self.c2rgb(col)
            self.colors[x] = self.rgb2c(max(r1, gauss*r), max(g1, gauss*g), max(b1, gauss*b))


class Evolver(object):
    def evolve(self, rate):
        pass

    def is_finished(self):
        return True


class LinearNumberEvolver(Evolver):
    def __init__(self, start, stop, duration):
        self.value = start
        self.d_value = float(stop-start)/duration
        self.remaining_time = duration

    def evolve(self, rate):
        if self.is_finished():
            return

        self.value += self.d_value*rate
        self.remaining_time -= rate

    def is_finished(self):
        if self.remaining_time <= 0:
            return True

        return False

    def get_value(self):
        return self.value


class SawNumberEvolver(Evolver):
    def __init__(self, start, stop, period):
        self.min = start  # min doesn't need to be smaller than max
        self.max = stop
        self.period = period
        self.time = 0
        self.value = start

    def evolve(self, rate):
        self.time += rate

        if self.time < 0:
            self.time += self.period
        if self.time > self.period:
            self.time -= self.period

        half_time = 2.0*self.time/self.period
        delta = self.max-self.min
        if self.time <= self.period*0.5:
            self.value = self.min + delta*half_time
        else:
            self.value = self.max - delta*(half_time-1)

    def is_finished(self):
        return False

    def get_value(self):
        return self.value


class LinearHueColorEvolver(LinearNumberEvolver):
    def get_value(self):
        r, g, b = hls_to_rgb(self.value, 0.3, 1.0)
        return (int(r*255) << 16) | (int(g*255) << 8) | int(b*255)

class SawHueColorEvolver(SawNumberEvolver):
    def get_value(self):
        r, g, b = hls_to_rgb(self.value, 0.3, 1.0)
        return (int(r*255) << 16) | (int(g*255) << 8) | int(b*255)


class LedEffect(object):
    def apply(self, ledstrip):
        pass

class GaussPeakLedEffect(LedEffect, Evolver):

    def __init__(self, color, pos, sigma, duration=None):
        self.color = color
        self.pos = pos
        self.sigma = sigma
        self.remaining_time = duration or 0.0

    def apply(self, ledstrip):
        if self.is_finished():
            return

        color = self.color
        pos = self.pos
        sigma = self.sigma

        if isinstance(self.color, Evolver):
            color = self.color.get_value()

        if isinstance(self.pos, Evolver):
            pos = self.pos.get_value()

        if isinstance(self.sigma, Evolver):
            sigma = self.sigma.get_value()

        ledstrip.add_gauss(color, pos, sigma)

    def evolve(self, rate):
        if self.is_finished():
            return

        if isinstance(self.color, Evolver):
            self.color.evolve(rate)

        if isinstance(self.pos, Evolver):
            self.pos.evolve(rate)

        if isinstance(self.sigma, Evolver):
            self.sigma.evolve(rate)

        self.remaining_time -= rate

    def is_finished(self):
        if self.remaining_time is not None and self.remaining_time <= 0:
            return True

        return False


class LedStripSynthesizer(object):
    def __init__(self, ledstrip, fps):
        self.led_strip = ledstrip
        self.cycle = 1.0/fps
        self.stop = False

        self.effects = []

        self._thread = threading.Thread(target=self.run)
        self._thread.start()

    def run(self):
        while not self.stop:
            self.led_strip.start_composition()
            for effect in self.effects[:]:
                effect.apply(self.led_strip)
                effect.evolve(self.cycle)

                if effect.is_finished():
                    self.effects.remove(effect)

            self.led_strip.finish_composition()
            sleep(self.cycle)

        self.stop = False

    def add_effect(self, effect):
        self.effects.append(effect)
