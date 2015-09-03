from sys import argv
import socket
from select import select
from random import random

import pickle

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

    def setup(self):
        super().setup()
        self.socket.listen(5)

    def transfer(self, P):
        conn, addr = self.socket.accept()
        data = conn.recv(1024)
        if(data and random() >= P):
            self.socket_out.transfer(data)
        conn.close()


class Out_Channel_Socket(Channel_Socket):
    first_time = True
    #definition for outgoing port
    def __init__(self, port, port_to):
        self.port_to = port_to
        super().__init__(port)

    def transfer(self, data):
        if self.first_time:
            self.socket.connect((HOST, self.port_to))

        self.socket.send(data)


def main():

    args = argv

    if len(args) < 5:
        args = ["", 5001, 5002, 5003, 5004, 7001, 6001, 0]

    ports = args[1:7]

    if len(ports) > len(set(ports)):
        raise BaseException("Overlapping Ports")

    for i in range(len(ports)):
        ports[i] = int(ports[i])

    cs_in_port, cs_out_port, cr_in_port, cr_out_port = ports[0:4]
    s_in, r_in = ports[4:6]
    P = float(args[7])
    
    cs_out = Out_Channel_Socket(cs_out_port, r_in)
    cs_in = In_Channel_Socket(cs_in_port, cs_out)
    cr_out = Out_Channel_Socket(cr_out_port, s_in)
    cr_in = In_Channel_Socket(cr_in_port, cr_out)

    for channel_socket in [cs_in, cs_out, cr_in, cr_out]: 
        channel_socket.setup()

    while True:
        print("Waiting...")
        read_sockets = select([cr_in.socket, cs_in.socket], [], [])[0]
        print("Received", read_sockets)
        for in_sock in [cr_in, cs_in]:
            if in_sock.socket in read_sockets:
                in_sock.transfer(P)


main()