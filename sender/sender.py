﻿from sys import argv
from Packet import *
import socket
import os.path
import pickle
from select import select

HOST = socket.gethostname()

def setup_socket(port):
    if not (1024 <= port and port <= 64000):
            raise BaseException("Invalid Port")

    cur_socket = socket.socket()
    cur_socket.bind((HOST, port))
    return cur_socket

def make_packet(bytes, next):
    n = len(bytes)

    if n == 0:
        return Packet(PacketTypes.dataPacket, next, 0, []), True
        
    if 0 < len(bytes):
        return Packet(PacketTypes.dataPacket, next, n, bytes), False

def main():

    args = argv

    if len(args) < 5:
        args = ["", 7001, 7002, 5001, "to_send.txt"]

    ports = args[1:4]

    if ( len(ports) > len(set(ports)) ):
        raise BaseException("Overlapping Ports")

    for i in range(len(ports)):
        ports[i] = int(ports[i])

    s_in_port, s_out_port = ports[0:2]
    cs_in = ports[2]

    filename = args[4]

    s_in = setup_socket(s_in_port)
    s_out = setup_socket(s_out_port)

    s_in.listen(5)
    s_in.settimeout(1.0)
    
    s_out.connect((HOST, cs_in))

    if( not os.path.isfile(filename) ):
        raise BaseException("File does not exist")

    next = 0
    exitFlag = False

    file = open(filename, mode="rb")

    while not exitFlag:
        bytes = file.read(512)
        packet, exitFlag = make_packet(bytes, next)
        pickled = pickle.dumps(packet)

        while True:
            s_out.send(pickled)
            
            try:
                conn, addr = s_in.accept()
            except:
                continue

            resp_pickled = conn.recv(1024)
            resp = pickle.loads(resp_pickled)

            if (resp.magicno == 0x497E and 
                resp.type == PacketTypes.acknowledgementPacket and
                resp.dataLen == 0 and
                resp.next == next):
                next += 1
                break
            print('close')
            conn.close()

    s_out.close()
    file.close()
    print(next)


main()