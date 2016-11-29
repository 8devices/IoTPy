import platform
import glob
import serial
from IoTPy.sfp import encode_sfp, decode_sfp
from IoTPy.errors import IoTPy_APIError
from uuid import UUID


def detect_sfp_serial(uid=None):
    ports_list = []
    my_platform = platform.system()
    if uid:
        uid = UUID(uid)

    if my_platform == "Windows":
        for i in range(256):
            try:
                serial_tmp = serial.Serial('COM'+str(i))
                ports_list.append(serial_tmp.portstr)
                serial_tmp.close()
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
                baudrate=230400,  # virtual com port on USB is always max speed
                parity=serial.PARITY_ODD,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
            komanda_siuntimui = encode_sfp(255, [])
            port_to_try.write(komanda_siuntimui)
            response = port_to_try.read(1)    # read one, blocking
            n = port_to_try.inWaiting()        # look if there is more
            if n:
                response = response + port_to_try.read(n)
                sfp = decode_sfp(response)

                if sfp[0] == 255:  # device info sfp packet
                    dev_uid = UUID(bytes=sfp[1][1])
                    if not uid or uid == dev_uid:
                        return port_to_try

            port_to_try.close()
        except:
            pass

    raise IoTPy_APIError("No SFP device was found on serial ports.")
