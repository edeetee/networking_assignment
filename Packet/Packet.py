class PacketTypes:
    dataPacket = "dataPacket"
    acknowledgementPacket = "acknowledgementPacket"

class Packet:
    #definition for packet class
    
    def __init__(self, packetType, seqno, dataLen, data):
        #define magicno here so that class definition cannot override
        self.magicno = 0x497E
        self.type = PacketTypes(packetType)
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data