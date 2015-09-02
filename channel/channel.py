from sys import argv
import socket
from select import select
from random import random

HOST = socket.gethostname()

class Channel_Socket:
    #generic definition for channel socket
    def __init__(self, port):
        self.port = int(port)

    def setup(self):
        if not (1024 <= self.port and self.port <= 64000):
            raise BaseException("Invalid Port")

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

    if ( len(argv) > len(set(argv)) ):
        raise BaseException("Overlapping Ports")

    for i in range(1, 7):
        argv[i] = int(argv[i][:-1])

    cs_in_port, cs_out_port, cr_in_port, cr_out_port = argv[1:5]

    s_in, r_in = argv[5:7]
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