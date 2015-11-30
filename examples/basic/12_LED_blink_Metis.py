from time import sleep
from IoTPy.boards.metis import Metis
from IoTPy.interfaces.gpio import GPIO
from IoTPy.transport import SerialTransport, SocketTransport

# This is platform dependent - please configure to your application
LED_PIN_ID = 'D16'
io = SerialTransport()
with Metis(io) as board, board.digital(LED_PIN_ID) as ledPin:
    ledPin.setup(GPIO.OUTPUT)  # set digital pin to be output
    try:
        while True:
            ledPin.write(1)  # Turn led ON
            sleep(0.2)
            ledPin.write(0)  # Turn led OFF
            sleep(0.2)
    except KeyboardInterrupt:
        ledPin.write(0)  # Turn led OFF
        pass