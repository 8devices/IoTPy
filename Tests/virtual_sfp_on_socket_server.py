import socket
import sys
from IoTPy.SFPprocessor import SfpMachine

HOST = None              # Symbolic name meaning all available interfaces
PORT = 7777              # Arbitrary non-privileged port

s = None
sfp_machine_instance = SfpMachine()

for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM,
        0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        command_list = data.split(b'\xd4')
        command_list.remove('')
        for sfp_command in command_list:
            sfp_machine_result = sfp_machine_instance.execute_sfp(b'\xd4'+sfp_command)
            if sfp_machine_result:
                conn.send(sfp_machine_result)
    conn.close()
