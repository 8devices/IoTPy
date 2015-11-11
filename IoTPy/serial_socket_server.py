# based on pyserial example
import sys
import threading
import socket
from detect_sfp_serial import detect_sfp_serial


class Redirector:
    def __init__(self, serial_instance, socket):
        self.serial = serial_instance
        self.socket = socket
        self._write_lock = threading.Lock()
        self.alive = True
        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.setDaemon(True)
        self.thread_read.setName('serial->socket')
        self.thread_read.start()
        self.writer()

    def reader(self):
        """loop forever and copy serial->socket"""
        while self.alive:
            try:
                data = self.serial.read(1)              # read one, blocking
                n = self.serial.inWaiting()             # look if there is more
                if n:
                    data = data + self.serial.read(n)   # and get as much as possible
                if data:
                    self._write_lock.acquire()
                    try:
                        self.socket.sendall(data)           # send it over TCP
                    finally:
                        self._write_lock.release()
            except socket.error, msg:
                sys.stderr.write('ERROR: %s\n' % msg)
                # probably got disconnected
                break
        self.alive = False

    def write(self, data):
        """thread safe socket write with no data escaping. used to send telnet stuff"""
        self._write_lock.acquire()
        try:
            self.socket.sendall(data)
        finally:
            self._write_lock.release()

    def writer(self):
        """loop forever and copy socket->serial"""
        while self.alive:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                self.serial.write(data)                 # get a bunch of bytes and send them
            except socket.error, msg:
                sys.stderr.write('ERROR: %s\n' % msg)
                # probably got disconnected
                break
        self.alive = False
        self.thread_read.join()

    def stop(self):
        """Stop copying"""
        if self.alive:
            self.alive = False
            self.thread_read.join()


LOCAL_PORT = 7777
ser = detect_sfp_serial()
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind(('', LOCAL_PORT))
srv.listen(1)
while True:
    try:
        sys.stderr.write("Waiting for connection on %s...\n" % LOCAL_PORT)
        connection, addr = srv.accept()
        sys.stderr.write('Connected by %s\n' % (addr,))
        Redirector(ser, connection)
        sys.stderr.write('Disconnected\n')
        connection.close()
    except KeyboardInterrupt:
        break
    except socket.error, msg:
        sys.stderr.write('ERROR: %s\n' % msg)
sys.stderr.write('\n--- exit ---\n')
