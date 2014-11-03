

class GPIO:
    """
    This is a template class for IoTPy modules with GPIO functionality. Each such module should implement
    :class:`GPIO` functions according to their description.
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
    NONE = 0
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

        :param direction:  GPIO direction (:const:`GPIO.INPUT` or :const:`GPIO.OUTPUT`)
        :param resistor: Type of resistor to use when GPIO is in INPUT mode (:const:`GPIO.NONE`,
         :const:`GPIO.PULL_UP` or :const:`GPIO.PULL_DOWN`)
        :return: None
        """
        raise NotImplementedError()

    def read(self):
        raise NotImplementedError()

    def write(self, value):
        raise NotImplementedError()

    def attach_irq(self, event, callback=None, user_object=None, debounce_time=50):
        raise NotImplementedError()

    def detach_irq(self):
        raise NotImplementedError()

    def get_irq_count(self):
        raise NotImplementedError()

    def clear_irq_count(self, clear_to=0):
        raise NotImplementedError()


class GPIOProducer:

    def GPIO(self, name, *args, **kwargs):
        raise NotImplementedError()
