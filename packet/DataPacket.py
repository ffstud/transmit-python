from packet.Packet import *

class DataPacket(Packet):
    def __init__(self, transmission_id, sequence_number, data):
        super().__init__(transmission_id, sequence_number)
        self.data = data

    def serialize(self):
        header = super().serialize()
        byte_buffer = bytearray()
        byte_buffer.extend(header)
        byte_buffer.extend(self.data)
        return byte_buffer

    @classmethod
    def deserialize(cls, data):
        transmission_id_bytes = data[:2]
        transmission_id = int.from_bytes(transmission_id_bytes, byteorder='big')

        sequence_number_bytes = data[2:6]
        sequence_number = int.from_bytes(sequence_number_bytes, byteorder='big')
        payload = data[6:]
        return cls(transmission_id, sequence_number, payload)

    def __str__(self):
        return f"DataPacket{{data={self.data}, " \
               f"transmission_id={self.transmission_id}, " \
               f"sequence_number={self.sequence_number}}}"

