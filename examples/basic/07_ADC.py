from colorsys import hls_to_rgb
from IoTPy.pyuper.adc import ADC
from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.pwm import PWM

with IoBoard() as uper, \
        ADC(uper, 23) as adcPin1, ADC(uper, 24) as adcPin2, \
        PWM(uper, 27) as redPin, PWM(uper, 28) as greenPin, PWM(uper, 34) as bluePin:

    while True:
        hue = float(adcPin1.read())/1023
        lightness = float(adcPin2.read())/1024

        rgb = hls_to_rgb(hue, lightness, 1)

        redPin.write(rgb[0])
        greenPin.write(rgb[1])
        bluePin.write(rgb[2])