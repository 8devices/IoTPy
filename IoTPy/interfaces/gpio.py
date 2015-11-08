from IoTPy.errors import IoTPy_APIError, errmsg
from IoTPy.pinmaps import CAP_GPIO
from IoTPy.sfp import encode_sfp, decode_sfp
import struct


class GPIO(object):
    """
    GPIO (General Purpose Input and Output) pin module.

    :param board: IoBoard to which the pin belongs to.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param pin: GPIO pin number.
    :type pin: int
    :raise: IoTPy_APIError
    """
    # digital pin directions
    INPUT = 0
    """ INPUT direction constant"""
    OUTPUT = 1
    """ OUTPUT direction constant"""

    # GPIO resistors
    HIGH_Z = NONE = 0
    """ no-pull (high-z) resistor constant """
    PULL_UP = 1
    """ pull-up resistor constant """
    PULL_DOWN = 2
    """ pull-down resistor constant """

    # digital pin events
    LOW = 0
    HIGH = 1
    CHANGE = 2
    RISE = 3
    FALL = 4

    def __init__(self, board, pin):
        self.board = board
        if self.board.pinout[pin].capabilities & CAP_GPIO:
            self.logical_pin = self.board.pinout[pin].pinID
        else:
            errmsg("UPER API: Pin No:%d is not GPIO pin.", pin)
            raise IoTPy_APIError("Trying to assign GPIO function to non GPIO pin.")

        # Configure default state to be input with pull-up resistor
        self.board.lowlevel_io(0, encode_sfp(1, [self.logical_pin]))  # set primary
        self.direction = self.INPUT
        self.resistor = self.PULL_UP
        self.setup(self.direction, self.resistor) # default GPIO pin state is INPUT and PULL_UP

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.detach_irq()
        pass

    def setup(self, direction, resistor=PULL_UP):
        """
        Configure GPIO.

        :param direction: GPIO direction: GPIO.OUTPUT or GPIO.INPUT
        :param resistor: GPIO internal resistor mode. Used when direction is GPIO.INPUT. Should be GPIO.PULL_UP, \
        GPIO.PULL_DOWN or GPIO.NONE.

        :raise: IoTPy_APIError
        """
        if not direction in [self.OUTPUT, self.INPUT]:
            raise IoTPy_APIError("Invalid digital pin direction. Should be INPUT or OUTPUT")

        if direction == self.INPUT and not resistor in [self.NONE, self.PULL_UP, self.PULL_DOWN]:
            raise IoTPy_APIError("Invalid digital pin resistor setting. Should be GPIO.NONE, GPIO.PULL_UP or GPIO.PULL_DOWN")

        self.direction = direction

        if direction == self.INPUT:
            self.resistor = resistor

            if resistor == self.PULL_UP:
                mode = 4  # PULL_UP
            elif resistor == self.PULL_DOWN:
                mode = 2  # PULL_DOWN
            else:
                mode = 0  # HIGH_Z
        else:
            mode = 1  # OUTPUT

        self.board.lowlevel_io(0, encode_sfp(3, [self.logical_pin, mode]))

    def write(self, value):
        """
        Write a digital value (0 or 1). If GPIO pin is not configured as output, set it's GPIO mode to GPIO.OUTPUT.

        :param value: Digital output value (0 or 1)
        :type value: int
        """
        if self.direction != self.OUTPUT:
            self.setup(self.OUTPUT)
        self.board.lowlevel_io(0, encode_sfp(4, [self.logical_pin, value]))

    def read(self):
        """
        Read a digital signal value. If GPIO pis in not configure as input, set it to GPIO.PULL_UP pin mode.

        :return: Digital signal value: 0 (LOW) or 1 (HIGH).
        :rtype: int
        """
        if self.direction != self.INPUT:
            self.setup(self.INPUT, self.resistor)
        return decode_sfp(self.board.lowlevel_io(1, encode_sfp(5, [self.logical_pin])))[1][1]

    def attach_irq(self, event, callback=None, user_object=None, debounce_time=50):
        """
        Attach (enable) or reconfigure GPIO interrupt event.

        :param event: GPIO interrupt event. Can have one of these values: GPIO.RISE, GPIO.FALL, GPIO.CHANGE, \
        GPIO.LOW or GPIO.HIGH.
        :param callback: User callback function. This function is executed when the interrupt event is received. \
        It should take two arguments: interrupt event description and user object. Interrupt event descriptor is \
        dictionary with three fields: 'id' - the interrupt ID (interrupt channel), 'event' - interrupt event type \
        and 'values' - the logical values on each of interrupt channel (N-th bit represents logical pin value of \
        interrupt channel N). User object is the same object as user_object.
        :param user_object: User defined object, which will be passed back to the callback function. Optional,  \
        default is None.
        :param debounce_time: Interrupt disable time in milliseconds after the triggering event. This is used to \
        "debounce" buttons or to protect communication channel from data flood. Optional, default is 50ms.

        :return: Logical interrupt ID
        :rtype: int
        :raise: IoTPy_APIError
        """
        try:
            irq_id = self.board.interrupts.index(self.logical_pin)
            self.board.lowlevel_io(0, encode_sfp(7, [irq_id])) 	# detach interrupt
        except ValueError:
            try:
                irq_id = self.board.interrupts.index(None)
                self.board.interrupts[irq_id] = self.logical_pin
            except ValueError:
                errmsg("UPER API: more than 8 interrupts requested")
                raise IoTPy_APIError("Too many interrupts.")
        self.board.callbackdict[self.logical_pin] = {'mode': event, 'callback': callback, 'userobject': user_object}
        self.board.lowlevel_io(0, encode_sfp(6, [irq_id, self.logical_pin, event, debounce_time]))
        return irq_id

    def detach_irq(self):
        """
        Detach (disable) GPIO interrupt.

        :return: True on success, False otherwise
        :raise: IoTPy_APIError
        """
        try:
            irq_id = self.board.interrupts.index(self.logical_pin)
        except ValueError:
            #errmsg("UPER API: trying to detach non existing interrupt.")
            return False

        self.board.interrupts[irq_id] = None
        del self.board.callbackdict[self.logical_pin]
        self.board.lowlevel_io(0, encode_sfp(7, [irq_id]))
        return True

    def get_irq_count(self):
        raise NotImplementedError()

    def clear_irq_count(self, clear_to=0):
        raise NotImplementedError()

    def read_pulse(self, level=HIGH, timeout=100000):
        if self.direction != self.INPUT:
            self.setup(self.INPUT, self.resistor)

        return decode_sfp(self.board.lowlevel_io(1, encode_sfp(9, [self.logical_pin, level, timeout])))[1][0]


class GPIOPort(object):
    """
    GPIOPort (General Purpose Input and Output) port module.

    :param board: IoBoard to which the pin belongs to.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param pins: GPIO pin numbers.
    :type pins: list
    :raise: IoTPy_APIError
    """

    def __init__(self, board, pins):
        self.board = board

        for pin in pins:
            if not self.board.pinout[pin].capabilities & CAP_GPIO:
                raise IoTPy_APIError("Trying to assign GPIO function to non GPIO pin.")

        self._logical_pins = list(self.board.pinout[pin].pinID for pin in pins)
        self._logical_pins = struct.pack("B"*len(self._logical_pins), *self._logical_pins)

        # Configure default state to be input with pull-up resistor
        self.direction = GPIO.INPUT
        self.resistor = GPIO.PULL_UP
        self.setup(self.direction, self.resistor)
        self.board.lowlevel_io(0, encode_sfp(1, [self._logical_pins]))  # set primary

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def setup(self, direction, resistor=GPIO.PULL_UP):
        if not direction in [self.OUTPUT, self.INPUT]:
            raise IoTPy_APIError("Invalid digital pin direction. Should be INPUT or OUTPUT")

        if direction == self.INPUT and not resistor in [GPIO.NONE, GPIO.PULL_UP, GPIO.PULL_DOWN]:
            raise IoTPy_APIError("Invalid GPIO resistor setting. Should be GPIO.NONE, GPIO.PULL_UP or GPIO.PULL_DOWN")

        self.direction = direction

        if direction == self.INPUT:
            self.resistor = resistor

            if resistor == self.PULL_UP:
                mode = 4  # PULL_UP
            elif resistor == self.PULL_DOWN:
                mode = 2  # PULL_DOWN
            else:
                mode = 0  # HIGH_Z
        else:
            mode = 1  # OUTPUT

        self.board.lowlevel_io(0, encode_sfp(3, [self._logical_pins, chr(mode)*len(self._logical_pins)]))

    def write(self, value):
        """
        Write a digital port value. If GPIO port is not configured as output, set it's GPIO mode to GPIO.OUTPUT.

        :param value: Digital output value
        :type value: int
        """
        if self.direction != GPIO.OUTPUT:
            self.setup(GPIO.OUTPUT)

        values = list(((value >> i) & 1) for i in xrange(len(self._logical_pins)))
        values = struct.pack("B"*len(self._logical_pins), *values)

        self.board.lowlevel_io(0, encode_sfp(4, [self._logical_pins, values]))

    def read(self):
        """
        Read a digital port value. If GPIO port in not configure as input, set it to GPIO.PULL_UP pin mode.

        :return: Digital port value.
        :rtype: int
        """
        if self.direction != GPIO.INPUT:
            self.setup(GPIO.INPUT, self.resistor)

        values = decode_sfp(self.board.lowlevel_io(1, encode_sfp(5, [self._logical_pins])))[1][1]
        value = 0
        for i, bit in enumerate(values):
            value |= (ord(bit) & 0x1) << i

        return value
