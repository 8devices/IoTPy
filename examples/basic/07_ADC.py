from colorsys import hls_to_rgb

from IoTPy.boards.uper import UPER1

with UPER1() as board, \
        board.analog("ADC0") as adcPin1, board.analog("ADC1") as adcPin2, \
        board.pwm("PWM0_0") as redPin, board.pwm("PWM0_1") as greenPin, board.pwm("PWM0_2") as bluePin:

    while True:
        hue = adcPin1.read()
        lightness = adcPin2.read()

        rgb = hls_to_rgb(hue, lightness, 1)

        redPin.set_duty_cycle(rgb[0]*100)
        greenPin.set_duty_cycle(rgb[1]*100)
        bluePin.set_duty_cycle(rgb[2]*100)