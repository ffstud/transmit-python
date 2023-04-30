from packet.util.PacketInterpreter import *
from packet.Packet import *

class FinalizePacket(Packet):
    def __init__(self, transmission_id: int, sequence_number: int, md5: bytes):
        super().__init__(transmission_id, sequence_number)
        self.md5 = md5

    def get_md5(self):
        return self.md5

    def serialize(self):
        header = super().serialize()
        packet_data = struct.pack(f"16s", self.md5)
        return header + packet_data

    def __str__(self):
        return f"FinalizePacket{{md5={self.md5.hex()}, transmissionId={self.transmission_id}, sequenceNumber={self.sequence_number}}}"

