

class GPIO(object):
    """
    This is an IoTPy core class for modules (pins) with GPIO functionality.
    Usually GPIO modules will be a part of a device or board. In these cases the device (or board) should
    implement :class:`GPIOProducer` class and :func:`IoTPy.core.gpio.GPIOProducer.GPIO` method be called
    to retrieve an underlying GPIO module.

    """

    # GPIO directions
    INPUT = 0
    """GPIO INPUT direction constant"""
    OUTPUT = 1
    """GPIO OUTPUT direction constant"""

    # GPIO resistors
    HIGH_Z = NONE = 0
    """ GPIO no-pull (high-z) resistor constant """
    PULL_UP = 1
    """ GPIO pull-up resistor constant """
    PULL_DOWN = 2
    """ GPIO pull-down resistor constant """

    # GPIO events
    LOW = 0
    HIGH = 1
    CHANGE = 2
    RISE = 3
    FALL = 4

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError()

    def setup(self, direction, resistor=PULL_UP):
        """setup(direction, resistor=:const:`GPIO.PULL_UP`)
        Configure GPIO pin direction and pull resistors.

        :param direction: GPIO direction (:const:`GPIO.INPUT` or :const:`GPIO.OUTPUT`)
        :param resistor: Type of resistor to use when GPIO is in INPUT mode (:const:`GPIO.NONE`,
         :const:`GPIO.PULL_UP` or :const:`GPIO.PULL_DOWN`)
        """
        raise NotImplementedError()

    def read(self):
        """
        Read and return digital input value.

        :return: Digital signal value (:const:`GPIO.LOW` or :const:`GPIO.HIGH`)
        :rtype: int
        """
        raise NotImplementedError()

    def write(self, value):
        """
        Set digital output value.

        :param value: Digital signal value (:const:`GPIO.LOW` or :const:`GPIO.HIGH`).
        :type value: int
        """
        raise NotImplementedError()

    def attach_irq(self, event, callback=None, user_object=None, debounce_time=50):
        """
        Attach (enable) and configure GPIO interrupt event on this GPIO pin.

        :param event: Interrupt event type (:const:`GPIO.FALL` - trigger on falling edge, :const:`GPIO.RISE` - trigger
         on rising edge, :const:`GPIO.CHANGE` - trigger on rising or falling edge, :const:`GPIO.LOW` - trigger on low
         level, :const:`GPIO.HIGH` - trigger on HIGH level).
        :param callback: User defined callback function. When the interrupt is triggered, a
         callback(irq_event, user_object) call is executed. An irq_event is dictionary with three fields:
         'id' - the interrupt channel ID, 'event' - interrupt event type and 'values' - the digital signal
         values on each of the interrupt channels (N-th bit represents corresponds to interrupt channel N).
        :param user_object: User defined object.
        :param debounce_time: Interrupt inactivity (after trigger) time  in milliseconds. This is used to prevent
         from calling a callback function too often or to debounce buttons.
        :return: An interrupt channel ID.
        :rtype: int
        """
        raise NotImplementedError()

    def detach_irq(self):
        """
        Disable GPIO interrupt events on this pin.

        :return: True on success, False otherwise
        :rtype: bool
        """
        raise NotImplementedError()

    def get_irq_count(self):
        """
        Return a number of interrupt events that happened after the last attach_irq or clear_irq_count calls.

        :return: A number of interrupt events.
        :rtype: int
        """
        raise NotImplementedError()

    def clear_irq_count(self, initial_value=0):
        """
        Reset interrupt event count (counter value) to 0 or initial_value.

        :param initial_value: Initial interrupt event count value.
        :type initial_value: int
        """
        raise NotImplementedError()


class GPIOPort(GPIO):
    """
    Experimental, to be defined class.
    For now it is a class that acts as a set of parallel GPIO pins (GPIO port) which can be written or read in one call.
    """
    pass


class GPIOProducer(object):
    """
    This is a template class for boards or devices that produce a :class:`IoTPy.core.gpio.GPIO` module.
    """

    def GPIO(self, name, *args, **kwargs):
        """
        Create and return a GPIO module.

        :param name: Board specific identification name of the GPIO pin.
        :param args: Board specific positional arguments.
        :param kwargs: Board specific named arguments.
        :return: :class:`IoTPy.core.gpio.GPIO`
        """
        raise NotImplementedError()
