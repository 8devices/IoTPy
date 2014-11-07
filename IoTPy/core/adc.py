

class ADC(object):
    """
    This is a template class for IoTPy modules with ADC functionality. Each such module should implement
    :class:`ADC` functions according to their description.
    Usually ADC modules will be a part of a device or board. In these cases the device (or board) should
    implement :class:`ADCProducer` class and :func:`IoTPy.core.adc.ADCProducer.ADC` method be called
    to retrieve an underlying ADC module.

    """

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError()

    def read(self):
        """
        Read a fractional analog value.

        :return: A normalized value, ranging (inclusive) from 0.0 to 1.0 (max voltage).
        :rtype: float
        """
        raise NotImplementedError()

    def read_raw(self):
        """
        Read a raw ADC value. The maximum value depends on the underlying ADC's resolution: for 8-bit ADCs it's 255,
        for 10-bit it's 1023, etc.

        :return: A raw ADC value, as measured by the ADC module.
        :rtype: int
        """
        raise NotImplementedError()


class ADCProducer(object):
    """
    This is a template class for boards or devices that can produce an :class:`IoTPy.core.adc.ADC` module.
    """

    def ADC(self, name, *args, **kwargs):
        """
        Create and return an ADC module.

        :param name: Identification name of the ADC module. It is device specific and can be a string "ADC0"
         or simply an integer 0.
        :param args: Board specific positional arguments.
        :param kwargs: Board specific named arguments.
        :return: :class:`IoTPy.core.adc.ADC`
        """
        raise NotImplementedError()
