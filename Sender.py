import os
import socket
import hashlib
import math
import time

from packet.DataPacket import *
from packet.InitializePacket import *
from packet.FinalizePacket import *

class Sender:
    def __init__(self, file_to_transfer, receiver, port, packet_size, transmission_id, packet_delay_us):
        self.file_to_transfer = file_to_transfer
        self.receiver = receiver
        self.port = port
        self.packet_size = packet_size
        self.transmission_id = transmission_id
        self.packet_delay_us = packet_delay_us
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sequence_number = 0

    def send(self):
        file_size = self.file_to_transfer.seek(0, 2)

        # calculate maxSequenceNumber
        max_sequence_number = math.ceil(file_size/self.packet_size)

        # send first (initialize) packet
        initialize_packet = InitializePacket(self.transmission_id, self.sequence_number, max_sequence_number, os.path.basename(self.file_to_transfer.name))
        print("Sent initialize packet at:", int(time.time()*1000))
        self.send_packet(initialize_packet)
        self.sequence_number += 1

        # send data packets while computing the md5 hash
        md5 = hashlib.md5()
        with open(self.file_to_transfer.name, 'rb') as input_file:
            while True:
                chunk = input_file.read(self.packet_size)
                if not chunk:
                    break
                data_packet = DataPacket(self.transmission_id, self.sequence_number, chunk)
                self.send_packet(data_packet)
                md5.update(chunk)
                self.sequence_number += 1

        # send last (finalize) packet
        finalize_packet = FinalizePacket(self.transmission_id, self.sequence_number, md5.digest())
        print("Sent finalize packet at:", int(time.time()*1000))
        self.send_packet(finalize_packet)

    def send_packet(self, packet):
        # convert packet to bytes
        packet_bytes = packet.serialize()

        # create UDP packet
        udp_packet = struct.pack("!%ds" % len(packet_bytes), packet_bytes)
        self.socket.sendto(udp_packet, (self.receiver, self.port))

        time.sleep(self.packet_delay_us / 1000000)

        print("Sent packet:")
        print(packet)
