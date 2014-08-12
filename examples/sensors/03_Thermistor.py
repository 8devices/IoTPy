from colorsys import hls_to_rgb
from IoTPy.pyuper.ioboard import IoBoard


with IoBoard() as uper, \
        uper.ADC("ADC0") as adcPin1, \
        uper.PWM("PWM0_0") as redPin, uper.PWM("PWM0_1") as greenPin, uper.PWM("PWM0_2") as bluePin:

    while True:
        # average for better results
        adc_sum = 0
        for i in xrange(20):
            adc_sum += adcPin1.read()
        adc = adc_sum/20

        hue = 0.5 + (adc-0.5)*30  # convert ADC value to color
        hue = min(hue, 1.0)
        hue = max(hue, 0.0)
        rgb = hls_to_rgb(hue, 0.5, 1)

        redPin.set_duty_cycle(rgb[0]*100)
        greenPin.set_duty_cycle(rgb[1]*100)
        bluePin.set_duty_cycle(rgb[2]*100)
