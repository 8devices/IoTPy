from colorsys import hls_to_rgb
from IoTPy.pyuper.ioboard import IoBoard

with IoBoard() as uper, \
        uper.ADC("ADC0") as adcPin1, uper.ADC("ADC1") as adcPin2, \
        uper.PWM("PWM0_0") as redPin, uper.PWM("PWM0_1") as greenPin, uper.PWM("PWM0_2") as bluePin:

    while True:
        hue = adcPin1.read()
        lightness = adcPin2.read()

        rgb = hls_to_rgb(hue, lightness, 1)

        redPin.set_duty_cycle(rgb[0]*100)
        greenPin.set_duty_cycle(rgb[1]*100)
        bluePin.set_duty_cycle(rgb[2]*100)