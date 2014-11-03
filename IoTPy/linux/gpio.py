from IoTPy.core.gpio import GPIO


class LinuxGPIO(GPIO):

    def __init__(self, pin):
        self.pin = pin

    def __enter__(self):
        with open("/sys/class/gpio/export", 'w') as export:
            export.write("%s" % self.pin)
            export.flush()

        self._value = open("/sys/class/gpio/gpio%s/value" % self.pin, 'w+')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._value.close()
        with open("/sys/class/gpio/unexport", 'w') as unexport:
            unexport.write("%s" % self.pin)
            unexport.flush()

    def setup(self, direction, resistor=GPIO.PULL_UP):
        if direction == GPIO.INPUT:
            _dir = 'in'
        elif direction == GPIO.OUTPUT:
            _dir = 'out'
        else:
            raise ValueError("Invalid direction value %s. Must be GPIO.INPUT or GPIO.OUTPUT.")

        self.direction = direction

        with open("/sys/class/gpio/gpio%s/direction" % self.pin, 'w') as direction:
            direction.write(_dir)
            direction.flush()

    def read(self):
        if self.direction != self.INPUT:
            self.setup(GPIO.INPUT)

        val = self._value.read()
        if val:
            return int(val)

    def write(self, value):
        if self.direction != GPIO.OUTPUT:
            self.setup(GPIO.OUTPUT)

        self._value.write('1' if value else '0')
        self._value.flush()
