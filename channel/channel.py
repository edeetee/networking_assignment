import Packet
from sys import argv
import socket

def valid_port(port):
    if not (1024 <= port and port <= 64000):
        raise Exception("Invalid Port")



def main():
    host = socket.gethostname()

    cs_in, cs_out, cr_in, cr_out, s_in, r_in, P = argv[1:]

    for port in [cs_in, cs_out, cr_in, cr_out]: valid_port(port)

    cs_in_socket = 

    


main()