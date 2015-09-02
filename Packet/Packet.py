class PacketTypes:
    dataPacket = "dataPacket"
    acknowledgementPacket = "acknowledgementPacket"

class Packet:
    #definition for packet class

    magicno = 0x497E
    
    def __init__(self, packetType, seqno, dataLen, data):
        self.type = PacketTypes(packetType)
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data