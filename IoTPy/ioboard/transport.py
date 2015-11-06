import platform
import glob
import serial
from IoTPy.ioboard.utils import IoTPy_APIError
from IoTPy.ioboard.sfp import decode_sfp, encode_sfp


class SerialTransport:
    def __init__(self, serial_port = None):
        self.serial_port = serial_port
        if not self.serial_port:
            ports_list = []
            my_platform = platform.system()
            if my_platform == "Windows":
                for i in range(256):
                    try:
                        self.serial_port = serial.Serial('COM'+str(i))
                        ports_list.append(self.serial_port.portstr)
                        self.serial_port.close()
                    except serial.SerialException:
                        pass
            elif my_platform == "Darwin":
                ports_list = glob.glob("/dev/tty.usbmodem*")
            elif my_platform == "Linux":
                ports_list = glob.glob("/dev/ttyACM*")

            for my_port in ports_list:
                try:
                    port_to_try = serial.Serial(
                        port=my_port,
                        baudrate=230400,  #virtual com port on USB is always max speed
                        parity=serial.PARITY_ODD,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=0.1
                    )
                    port_to_try.write(encode_sfp(255, []))
                    uper_response = port_to_try.read(1)    # read one, blocking
                    n = port_to_try.inWaiting()        # look if there is more
                    if n:
                        uper_response = uper_response + port_to_try.read(n)
                        if decode_sfp(uper_response)[0] == 255:  # found port with UPER
                            self.serial_port = port_to_try
                            break
                    port_to_try.close()
                except:
                    raise IoTPy_APIError("Unrecoverable serial port error.")

        if not self.serial_port:
            raise IoTPy_APIError("No UPER found on USB/serial ports.")

    def read(self):
        data = self.serial_port.read(1)              #read one, blocking
        n = self.serial_port.inWaiting()             #look if there is more
        if n:
            data = data + self.serial_port.read(n)   #and get as much as possible
        return data

    def write(self, data):
        self.serial_port.write(data)

    def flush(self):
        self.serial_port.flush()

    def close(self):
        self.serial_port.close()