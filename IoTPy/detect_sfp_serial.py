import platform
import glob
import serial
from IoTPy.sfp import encode_sfp, decode_sfp
from IoTPy.errors import IoTPy_APIError


def detect_sfp_serial():
    ports_list = []
    serial_port = False
    my_platform = platform.system()
    if my_platform == "Windows":
        for i in range(256):
            try:
                serial_port = serial.Serial('COM'+str(i))
                ports_list.append(serial_port.portstr)
                serial_port.close()
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
            response = port_to_try.read(1)    # read one, blocking
            n = port_to_try.inWaiting()        # look if there is more
            if n:
                response = response + port_to_try.read(n)
                if decode_sfp(response)[0] == 255:  # found port with UPER
                    serial_port = port_to_try
                    break
            port_to_try.close()
        except:
            raise IoTPy_APIError("Unrecoverable serial port error.")

    if not serial_port:
        raise IoTPy_APIError("No SFP device was found on serial ports.")
    return serial_port