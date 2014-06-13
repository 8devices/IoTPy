from colorsys import hls_to_rgb
from IoTPy.pyuper.adc import ADC
from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.pwm import PWM

with IoBoard() as uper, \
        ADC(uper, 23) as adcPin1, \
        PWM(uper, 27) as redPin, PWM(uper, 28) as greenPin, PWM(uper, 34) as bluePin:

    while True:
        # average for better results
        adc_sum = 0
        for i in xrange(20):
            adc_sum += adcPin1.read()
        adc = float(adc_sum)/20

        hue = 0.5 + (adc/1023-0.5)*30  # convert ADC value to color
        hue = min(hue, 1.0)
        hue = max(hue, 0.0)

        rgb = hls_to_rgb(hue, 0.2, 1)

        redPin.write(rgb[0])
        greenPin.write(rgb[1])
        bluePin.write(rgb[2])