import Packet
from sys import argv
import socket

HOST = socket.gethostname()

class Channel_Socket:
    port = 0

    def __init__(self):
        self.type = type
        

    def setup(self):
        if not (1024 < port and port < 64000):
            raise BaseException("Invalid Port")

        self.socket = socket.socket()
        self.socket.bind((HOST, self.port))




def main():
    cs_in = Channel_Socket()
    cs_out = Channel_Socket()
    cr_in = Channel_Socket()
    cr_out = Channel_Socket()

    if not ( len(argv) > len(set(argv)) ):
        raise BaseException("Overlapping Ports")

    cs_in.port, cs_out.port, cr_in.port, cr_out.port, 
    s_in, r_in, P = argv[1:]

    for channel_socket in [cs_in, cs_out, cr_in, cr_out]: channel_socket.setup(s_in, r_in)

    cs_out.socket.connect((HOST, s_in))
    cr_out.socket.connect((HOST, r_in))


    


main()