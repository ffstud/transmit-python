from packet.Packet import *

class AcknowledgementPacket(Packet):
    def __init__(self, transmission_id, sequence_number):
        super().__init__(transmission_id, sequence_number)


    def serialize(self):
        return super().serialize()