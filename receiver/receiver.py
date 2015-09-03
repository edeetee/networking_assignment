import Packet
from sys import argv
from select import select
import os.path
import pickle
import socket

HOST = socket.gethostname()

class Receiver_Socket:

    def __init__(self,port):
        self.port = int(port)

    def setup(self):
        if (1024 > self.port or self.port > 64000):
            raise BaseException("Invalid Port")

        self.socket = socket.socket()
        self.socket.bind((HOST, self.port))
        
class In_Receiver_Socket(Receiver_Socket):
    #definition for incoming port
    def __init__(self, port):
        super().__init__(port)

    def setup(self):
        super().setup()
        self.socket.listen(5)

        

class Out_Receiver_Socket(Receiver_Socket):
    first_time = True
    #definition for outgoing port
    def __init__(self, port, port_to):
        self.port_to = port_to
        super().__init__(port)

    def setup(self):
        super().setup()

    def send(self, data):
        if first_time:
            self.socket.connect((HOST, self.port_to))
        self.socket.send(data)

        
def main():
    
    args = argv
    if len(args) < 4:
        args = [6001,6002,5003,'test']
    
    if  (len(args) > len(set(args)) ):
        raise BaseException("Overlapping Ports")
    
    r_in = args[0]
    r_out = args[1]
    cr_in = args[2]
    filename = args[3]
    
    r_out = Out_Receiver_Socket(r_out, cr_in)
    r_in = In_Receiver_Socket(r_in)
    
    for channel_socket in [r_out, r_in]: 
        channel_socket.setup()
    
    if not os.path.exists("dir/{}.txt".format(filename)):
        open("{}.txt".format(filename), "w")
    else:
        raise BaseException("File Already Exists")
    
    expected = 0
    finished = False

    while not finished:
        
        conn, addr = r_in.socket.accept()

        received_packet = pickle.loads(conn.recv(1024))
            
        if received_packet.magicno != 0x497E:
            raise BaseException("Incorrect Magicno")
            
        if received_packet.type != "dataPacket":
            raise BaseException("Incorrect Packet Type")
            
        if received_packet.seqno != expected:
            packet = Packet("acknowledgementPacket", received_packet.seqno,0,[])
            pickled = pickle.dumps(packet)
            r_out.send(pickled)
        else:
            packet = Packet("acknowledgementPacket", received_packet.seqno,0,[])
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