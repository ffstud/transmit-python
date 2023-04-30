import struct
import array
import codecs

class PacketInterpreter:
    @staticmethod
    def isInitializationPacket(udpPacket):
        return PacketInterpreter.getSequenceNumber(udpPacket) == 0

    @staticmethod
    def getSequenceNumber(data):
        return struct.unpack_from("!i", data, 2)[0]

    @staticmethod
    def getTransmissionId(data):
        return struct.unpack_from("!h", data, 0)[0]

    @staticmethod
    def getUIntAt(data, index):
        return struct.unpack_from("!I", data, index)[0]

    @staticmethod
    def getStringAt(data, index, length):
        return codecs.decode(data[index:index+length], "utf-8")

    @staticmethod
    def getByteArrayAt(data, index, length):
        return array.array('B', data[index:index+length]).tobytes()
