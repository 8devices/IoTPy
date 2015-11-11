import socket, time
from IoTPy.detect_sfp_serial import detect_sfp_serial


class SocketTransport(object):
    def __init__(self, host = '', port = 7777):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def read(self):
        data = self.socket.recv(1024)
        return data

    def write(self, data):
        self.socket.send(data)

    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()



class SerialTransport(object):
    def __init__(self, serial_port = None):
        self.serial_port = serial_port
        if not self.serial_port:
            self.serial_port = detect_sfp_serial()

    def read(self):
        data = self.serial_port.read(1)              #read one, blocking
        n = self.serial_port.inWaiting()             #look if there is more
        if n:
            data = data + self.serial_port.read(n)   #and get as much as possible
        return data

    def write(self, data):
        self.serial_port.write(data)

    def close(self):
        self.serial_port.close()