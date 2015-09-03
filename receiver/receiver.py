import Packet
from sys import argv
from select import select
import os.path
import pickle
import socket

HOST = socket.gethostname()

class Receiver_Socket:

    def __init__(self,port):
        self.port = port

    def setup_socket(self):
        port = int(port)
        
        if (1024 > port or port > 64000):
            raise BaseException("Invalid Port")

        self.socket = socket.socket()
        self.socket.bind((HOST, self.port))
        
class In_Receiver_Socket(Receiver_Socket):
    #definition for incoming port
    def __init__(self, port):
        super().__init__(port)
        
    #def transfer(self, P):
        #data = self.socket.recv(1024)
        #if data:
            #self.socket_out.transfer(data)    
        

class Out_Receiver_Socket(Receiver_Socket):
    #definition for outgoing port
    def __init__(self, port, port_to):
        self.port_to = port_to
        super().__init__(port)

    def setup(self):
        self.socket.connect((HOST, self.port_to))
        super().setup()

        
def main():
    
    if len(argv) < 4:
        argv = [6001,6002,5003,'test']
    
    if not ( len(argv) > len(set(argv)) ):
        raise BaseException("Overlapping Ports")
    
    r_in = argv[0]
    r_out = argv[1]
    cr_in = argv[2]
    filename = argv[3]
    
    r_out = Out_Receiver_Socket(r_out_port, cr_in)
    r_in = In_Receiver_Socket(r_in_port)
    
    for channel_socket in [r_out, r_in]: 
        channel_socket.setup()
    
    if not os.path.exists("dir/{}.txt".format(filename)):
        open("{}.txt".format(filename), "w")
    else:
        raise BaseException("File Already Exists")
    
    expected = 0
    finished = False

    while not finished:
        
        #wait for incoming packet
        
        if received_packet.magicno != "0x497E":
            raise BaseException("Incorrect Magicno")
        
        if received_packet.type != "dataPacket":
            raise BaseException("Incorrect Packet Type")
        
        if received_packet.seqno != expected:
            packet = Packet("acknowledgementPacket", rcvd,seqno,0,[])
            pickled = pickle.dumps(packet)
            r_out.send(pickled)
        elif received_packet.seqno == expected:
            packet = Packet("acknowledgementPacket", rcvd,seqno,0,[])
            pickled = pickle.dumps(packet)
            r_out.send(pickled)
            expected = 1 - expected
            
            if received_packet.dataLen > 0:
                "{}.txt".format(filename).write(received_packet.data)
            elif received_packet.dataLen == 0:
                "{}.txt".format(filename).close()
                # Then close all sockets & Exit program
                r_in.close
                r_out.close
                finished = True
                
                
            



main()