from packet.Packet import *

class InitializePacket(Packet):
    def __init__(self, transmission_id, sequence_number, max_sequence_number, file_name):
        super().__init__(transmission_id, sequence_number)
        self.max_sequence_number = max_sequence_number
        self.file_name = file_name

    def serialize(self):
        header = super().serialize()
        file_name_bytes = self.file_name.encode('utf-8')
        return header + self.max_sequence_number.to_bytes(4, byteorder='big') + file_name_bytes

    @classmethod
    def deserialize(cls, data):
        super_obj, max_sequence_number, file_name_bytes = super().deserialize(data)
        file_name = file_name_bytes.decode('utf-8')
        return cls(super_obj.transmission_id, super_obj.sequence_number, max_sequence_number, file_name)

    def __str__(self):
        return f"InitializePacket{{maxSequenceNumber={self.max_sequence_number}, fileName={self.file_name}, transmissionId={self.transmission_id}, sequenceNumber={self.sequence_number}}}"

