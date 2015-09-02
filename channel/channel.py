from sys import argv
import socket
from select import select
from random import random

HOST = socket.gethostname()

class Channel_Socket:
    #generic definition for channel socket
    def __init__(self, port):
        if not (1024 <= port and port <= 64000):
            raise BaseException("Invalid Port")
        self.port = int(port)

    def setup(self):

        self.socket = socket.socket()
        self.socket.bind((HOST, self.port))


class In_Channel_Socket(Channel_Socket):
    #definition for incoming port
    def __init__(self, port, socket_out):
        self.socket_out = socket_out
        super().__init__(port)

    def transfer(self, P):
        data = self.socket.recv(1024)
        if(data and random() >= P):
            self.socket_out.transfer(data)


class Out_Channel_Socket(Channel_Socket):
    #definition for outgoing port
    def __init__(self, port, port_to):
        self.port_to = port_to
        super().__init__(port)

    def setup(self):
        super().setup()
        self.socket.connect((HOST, self.port_to))

    def transfer(self, data):
        self.socket.send(data)


def main():

    ports = argv[1:7]

    if len(ports) > len(set(ports)):
        raise BaseException("Overlapping Ports")

    for port in ports:
        port = int(port)

    cs_in_port, cs_out_port, cr_in_port, cr_out_port = ports[0:4]
    s_in, r_in = ports[4:6]
    P = float(argv[7])
    
    cs_out = Out_Channel_Socket(cs_out_port, s_in)
    cs_in = In_Channel_Socket(cs_in_port, cs_out)
    cr_out = Out_Channel_Socket(cr_out_port, r_in)
    cr_in = In_Channel_Socket(cr_in_port, cr_out)

    for channel_socket in [cs_in, cs_out, cr_in, cr_out]: 
        channel_socket.setup()

    while True:
        print("Waiting...")
        read_sockets = select([cr_in.socket, cs_in.socket], [], [])[0]
        cr_in.transfer(P)
        cs_in.transfer(P)


main()