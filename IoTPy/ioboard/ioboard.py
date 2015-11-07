#!/usr/bin/env python
# encoding: utf-8
from IoTPy.core.spi import SPI
from IoTPy.ioboard.adc import IO_ADC
from IoTPy.ioboard.gpio import IO_GPIO, IO_GPIOPort
from IoTPy.ioboard.i2c import IO_I2C
from IoTPy.ioboard.pwm import IO_PWM
from IoTPy.ioboard.spi import IO_SPI
from IoTPy.ioboard.sfp import encode_sfp, decode_sfp
from IoTPy.ioboard.transport import SerialTransport
from IoTPy.ioboard.utils import errmsg, IoTPy_APIError

from six import string_types
import threading
import queue

__version__ = '0.01'

class IoBoard:
    """
    Micro controller based IO board with serial over USB class.

    :param pinout: A list describing physical board pin layout and capabilities.
    :type pinout: :class:`IoTPy.pyuper.pinouts.IoPinout`
    :param serial_port: Name of SFP command serial communications port.
    :type serial_port: str
    """

    def __init__(self, pinout, io = None):
        self.interrupts = [None] * 8
        self.callbackdict = {}
        if not io:
            io = SerialTransport()
        self.io = io
        self.outq = queue.Queue()
        self.reader = Reader(self.io, self.outq, self.internalCallBack, decode_sfp)

        self.devicename = "uper"
        self.version = __version__
        self.pinout = pinout

    def get_info(self):
        """
        Get IoBoard device name and version info.

        :return: Tuple containing board name and version.
        """
        return self.devicename, self.version

    def stop(self):
        """
        Stop all communications with the board and close serial communication port.

        :raise: IoTPy_APIError
        """

        #for i in range(7):
        #    self.detachInterrupt(i)
        try:
            self.reader.stop()
            self.io.close()
        except:
            raise IoTPy_APIError("UPER API: Serial/USB port disconnected.")

    def lowlevel_io(self, ret, output_buf):
        """

        :param ret:
        :param output_buf:
        :return:
        """
        #print(':'.join(hex(ord(n)) for n in output_buf))
        try:
            self.io.write(output_buf)
        except:
            raise IoTPy_APIError("Unrecoverable serial port writing error, dying.")
        data = None
        if ret != 0:
            try:
                data = self.outq.get(True, 1)
            except queue.Empty:
                raise IoTPy_APIError("IoTPy: Nothing to read on serial port exception.")
            #print('|'.join(hex(ord(n)) for n in data))
        return data

    def internalCallBack(self, interrupt_data):
        """

        :param interrupt_data:
        :return:
        """

        interrupt_event = { 'id':interrupt_data[0], 'type':interrupt_data[1] & 0xFF, 'values':interrupt_data[1] >> 8 }
        callback_entry = self.callbackdict[self.interrupts[interrupt_event['id']]]

        try:
            callback_entry['callback'](interrupt_event, callback_entry['userobject'])
        except Exception as e:
            errmsg("IoTPy Interrupt callback exception: %s" % e)
        return

    def get_device_info(self):
        """
        Return information about the device.

        :return: A list containing board type, major and minor firmware versions, 16 byte unique identifier, microcontroller part and bootcode version numbers.
        """
        result = decode_sfp(self.lowlevel_io(1, encode_sfp(255, [])))

        if result[0] != 255:
            errmsg("IoTPy error: get_device_info wrong code.")
            #raise IoTPy_APIError("")
        device_data = result[1]

        if device_data[0] >> 24 != 0x55:  # 0x55 = 'U'
            print("IoTPy error: getDeviceInfo unknown device/firmware type")
            return

        device_info = []
        #device_info.append("UPER")  # type
        device_info.append((device_data[0] & 0x00ff0000) >> 16) #fw major
        device_info.append(device_data[0] & 0x0000ffff) #fw minor
        device_info.append(device_data[1]) # 16 bytes long unique ID from UPER CPU
        device_info.append(device_data[2]) # UPER LPC CPU part number
        device_info.append(device_data[3]) # UPER LPC CPU bootload code version
        return device_info

    def reset(self):
        """
        Perform software restart.
        """
        self.lowlevel_io(0, encode_sfp(251, []))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def ADC(self, pin, *args, **kwargs):
        return IO_ADC(self, pin)

    def GPIO(self, name, *args, **kwargs):
        if not (isinstance(name, int) or isinstance(name, string_types)):
            raise IoTPy_APIError("GPIO name must be an integer.")
        return IO_GPIO(self, name)

    def GPIOPort(self, names, *args, **kwargs):
        for name in names:
            if not isinstance(name, int):
                raise IoTPy_APIError("GPIO name must be an integer.")
        return IO_GPIOPort(self, names)

    def I2C(self, name, *args, **kwargs):
        return IO_I2C(self)

    def PWM(self, pin, freq=100, polarity=1, *args, **kwargs):
        return IO_PWM(self, pin, freq, polarity)

    def SPI(self, name, clock=1000000, mode=SPI.MODE_0, *args, **kwargs):
        _names = {"SPI0": 0, "SPI1": 1}
        if isinstance(name, int):
            port = name
        elif isinstance(name, str):
            if _names.has_key(name):
                port = _names[name]
            else:
                raise IoTPy_APIError("Invalid SPI name %s. Must be one of %s." % (name, ", ".join(sorted(_names.keys()))))
        else:
            raise IoTPy_APIError("PWM name must be an integer or a string")

        divider = int(round(2.0e6/clock))

        return IO_SPI(self, port, divider, mode)


class Reader:
    def __init__(self, io, outq, callback, decodefun):
        self.io = io
        self.outq = outq
        self.callback = callback
        self.alive = True

        self.irq_available = threading.Condition()
        self.irq_requests = list()

        self.thread_irq = threading.Thread(target=self.interrupt_handler)
        self.thread_irq.start()

        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.setDaemon(1)
        self.thread_read.start()
        self.decodefun = decodefun

    def interrupt_handler(self):
        with self.irq_available:
            while self.alive:
                self.irq_available.wait(0.05)
                while len(self.irq_requests):
                    interrupt = self.irq_requests.pop(0)
                    try:
                        self.callback(interrupt[1])
                    except Exception as e:
                        errmsg("UPER API: Interrupt callback error (%s)" % e)

        self.alive = False

    def reader(self):
        while self.alive:
            try:
                data = self.io.read()
                if data:
                    if data[3:4] == b'\x08':               #check if it's interrupt event
                        interrupt = self.decodefun(data)
                        with self.irq_available:
                            self.irq_requests.append(interrupt)
                            self.irq_available.notify()
                    else:
                        self.outq.put(data)
            except:
                errmsg("UPER API: serial port reading error.")
                break
        self.alive = False

    def stop(self):
        if self.alive:
            self.alive = False
            self.thread_irq.join()
            self.thread_read.join()