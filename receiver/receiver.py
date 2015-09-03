from Packet import *
from sys import argv
from select import select
import os.path
import pickle
import socket

HOST = socket.gethostname()

def setup_socket(port):
    if not (1024 <= port and port <= 64000):
            raise BaseException("Invalid Port")

    cur_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cur_socket.bind((HOST, port))
    return cur_socket

        
def main():
    
    args = argv
    if len(args) < 4:
        args = [6001,6002,5003,'to_send.txt']
    
    if  (len(args) > len(set(args)) ):
        raise BaseException("Overlapping Ports")
    
    r_in = args[0]
    r_out = args[1]
    cr_in = args[2]
    filename = args[3]
    
    r_out = setup_socket(r_out)
    r_in = setup_socket(r_in)

    r_out.connect((HOST, cr_in))

    file = None
    
    if os.path.isfile(filename):
        if len(argv) < 5:
            os.remove(filename)
            file = open(filename, "wb")
        else:
            raise BaseException("File Already Exists")
    else:
        file = open(filename, "wb")
    
    expected = 0
    first_time = True

    while True:
        data, addr = r_in.recvfrom(1024)

        rcvd = pickle.loads(data)
            
        if (rcvd.magicno == 0x497E and
            rcvd.type == PacketTypes.dataPacket):

            packet = Packet(PacketTypes.acknowledgementPacket, rcvd.seqno, 0, [])
            pickled = pickle.dumps(packet)

            if first_time:
                first_time = False

            r_out.send(pickled)

            if rcvd.seqno == expected:
                expected = 1 - expected
                
                if rcvd.dataLen > 0:
                    file.write(rcvd.data)
                else:
                    file.close()
                    # Then close all sockets & Exit program
                    r_out.close()
                    break
                


main()
