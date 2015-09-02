from sys import argv
from Packet import *
import socket
import os.path
from select import select

HOST = socket.gethostname()

def setup_socket(port):
    if not (1024 <= port and port <= 64000):
            raise BaseException("Invalid Port")

    cur_socket = socket.socket()
    cur_socket.bind((HOST, self.port))
    return cur_socket

def main():

    ports = argv[1:4]

    if ( len(ports) > len(set(ports)) ):
        raise BaseException("Overlapping Ports")

    for port in ports:
        port = int(port)

    s_in_port, s_out_port = ports[0:2]
    cs_in = ports[2]

    filename = argv[4]

    s_in = setup_socket(s_in_port)
    s_out = setup_socket(s_out_port)
    
    s_out.connect((HOST, cs_in))

    if( not os.path.isfile(filename) ):
        raise BaseException("File does not exist")

    next = 0
    exitFlag = False

    io

    file = open(filename, mode="rb")

    while True:
        bytes = file.read(512)

        data_packet = Packet(PacketTypes.dataPacket, "next", 0, [])
        exitFlag = True
        
        if 0 < len(bytes):
            pass

main()