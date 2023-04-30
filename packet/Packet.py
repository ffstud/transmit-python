class Packet:
    HEADER_SIZE = 6

    def __init__(self, transmission_id, sequence_number):
        self.transmission_id = transmission_id
        self.sequence_number = sequence_number

    def serialize(self):
        byte_buffer = bytearray(self.HEADER_SIZE)
        byte_buffer[0:2] = self.transmission_id.to_bytes(2, byteorder='big')
        byte_buffer[2:6] = self.sequence_number.to_bytes(4, byteorder='big')
        return byte_buffer

    @classmethod
    def deserialize(cls, data):
        transmission_id = int.from_bytes(data[0:2], byteorder='big', signed=False)
        sequence_number = int.from_bytes(data[2:6], byteorder='big', signed=False)
        return cls(transmission_id, sequence_number)

    def __str__(self):
        return f"Packet{{transmission_id={self.transmission_id}, sequence_number={self.sequence_number}}}"
