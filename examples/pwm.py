from colorsys import hls_to_rgb
from time import sleep
from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.pwm import PWM
from IoTPy.pyuper.utils import IoTPy_APIError, die

try:
    u = IoBoard()
except IoTPy_APIError, e:  # seems can't establish connection with the UPER board
    details = e.args[0]
    die(details)

try:  # let's try to attach PWM object to non PWM pin
    a = u.get_pin(PWM, 23)
except IoTPy_APIError, e:  # got an exception, pin capabilities must be different from requested
    details = e.args[0]
    print details

with u.get_pin(PWM, 27) as R, u.get_pin(PWM, 28) as G, u.get_pin(PWM, 34) as B:
    R.width_us(0)
    R.width_us(2500)
    sleep(0.5)
    R.width_us(10000)
    sleep(0.5)
    R.write(0)
    sleep(0.5)
    R.write(0.25)
    sleep(0.5)
    R.write(0.9)
    print "Red LED duty is:", R.read()
    sleep(0.5)
    i = 0
    try:
        while True:
            for color in range(500):
                rgb = hls_to_rgb(color*0.002, 0.1, 1)
                R.write(rgb[0])
                G.write(rgb[1])
                B.write(rgb[2])
                i += 1
                if not (i % 1000):
                    print i
                #print "R:", R.read(), "G:", G.read(), "B:", B.read()
                #sleep(0.0005)
    except KeyboardInterrupt:
            R.width_us(0)
            G.width_us(0)
            B.width_us(0)
            u.stop()
            die("Keyboard interrupt.")
