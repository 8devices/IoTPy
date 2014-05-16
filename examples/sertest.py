import serial
from time import sleep
from IoTPy.pyuper.utils import IoTPy_APIError, die
i = 0
"""
port_to_try = serial.Serial(
    port='/dev/tty.usbmodem14131',
    baudrate=230400, #virtual com port on USB is always max speed
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1
)
"""
while True:
    try:

        port_to_try = serial.Serial(
            port='/dev/tty.usbmodem14131',
            baudrate=230400, #virtual com port on USB is always max speed
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.1
        )

        port_to_try.write('GetDeviceInfo()')
        uper_response = port_to_try.read()    #read one, blocking

        n = port_to_try.inWaiting()        #look if there is moreresp = port_to_try.read(33)
        if n:  #print "%r" % resp
            #pass
            uper_response = uper_response + port_to_try.read(n)  #
        i += 1
        if not (i % 10):
            print i, n, "%r" % uper_response
        port_to_try.flush()
        port_to_try.close()
        sleep(0.1)
    except:
        die("PYKSHT!")