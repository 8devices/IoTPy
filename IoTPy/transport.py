import socket
from IoTPy.detect_sfp_serial import detect_sfp_serial


class SocketTransport(object):
    def __init__(self, host='127.0.0.1', port=7777):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.host, self.port)
        self.socket.connect((self.host, self.port))

    def read(self):
        return self.socket.recv(1024)

    def write(self, data):
        self.socket.send(data)

    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()


class SerialTransport(object):
    def __init__(self, serial_port=None):
        self.serial_port = serial_port
        if not self.serial_port:
            self.serial_port = detect_sfp_serial()
        self.serial_port.setTimeout(None)

    def read(self):
        try:
            data = self.serial_port.read(1)              # read one, blocking
            n = self.serial_port.inWaiting()             # look if there is more
            if n:
                data = data + self.serial_port.read(n)   # and get as much as possible
            return data
        except(Exception):
            pass
#            print("Pyksht", e)
            return None

    def write(self, data):
        self.serial_port.write(data)

    def close(self):
        self.serial_port.close()
