import os
import socket
import hashlib
import math
import time
from packet.DataPacket import *
from packet.InitializePacket import *
from packet.FinalizePacket import *


class Sender:
    def __init__(self, file_to_transfer, receiver, port, packet_size, transmission_id, ack_port,
                 operating_mode, window_size):
        self.file_to_transfer = file_to_transfer
        self.receiver = receiver
        self.port = port
        self.packet_size = packet_size
        self.transmission_id = transmission_id
        self.operating_mode = operating_mode
        self.window_size = window_size
        self.sequence_number = 0
        self.ack_port = ack_port
        self.buffer_size = 65535
        if self.operating_mode != 0:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind(("", ack_port))
            self.window_buffer = {}
            self.socket.settimeout(5000)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send(self):
        file_size = os.path.getsize(self.file_to_transfer)

        # calculate maxSequenceNumber
        max_sequence_number = math.ceil(file_size / self.packet_size)

        # send first (initialize) packet
        initialize_packet = InitializePacket(self.transmission_id, self.sequence_number, max_sequence_number,
                                             os.path.basename(self.file_to_transfer))
        print("Sent initialize packet at:", int(time.time() * 1000))
        self.send_packet(initialize_packet)

        # wait for ack
        if self.operating_mode == 1 and not self.handleAcknowledgementPacket():
            return

        if self.operating_mode == 2 and len(self.window_buffer) == self.window_size:
            while not self.handleSlidingAcknowledgementPacket():
                pass

        self.sequence_number += 1

        # send data packets while computing the md5 hash
        md5 = hashlib.md5()
        with open(self.file_to_transfer, 'rb') as input_file:
            while True:
                chunk = input_file.read(self.packet_size)
                if not chunk:
                    break
                data_packet = DataPacket(self.transmission_id, self.sequence_number, chunk)
                self.send_packet(data_packet)
                md5.update(chunk)
                # wait for ack
                if self.operating_mode == 1 and not self.handleAcknowledgementPacket():
                    return
                if self.operating_mode == 2 and len(self.window_buffer) == self.window_size:
                    while not self.handleSlidingAcknowledgementPacket():
                        pass
                self.sequence_number += 1

        # send last (finalize) packet
        finalize_packet = FinalizePacket(self.transmission_id, self.sequence_number, md5.digest())
        print("Sent finalize packet at:", int(time.time() * 1000))
        self.send_packet(finalize_packet)

        # wait for ack
        if self.operating_mode == 1 and not self.handleAcknowledgementPacket():
            return

        if self.operating_mode == 2:
            while not self.handleSlidingAcknowledgementPacket():
                pass

        self.socket.close()

    def send_packet(self, packet):
        # convert packet to bytes
        packet_bytes = packet.serialize()

        # create UDP packet
        udp_packet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_packet.sendto(packet_bytes, (self.receiver, self.port))

        # print("Sent packet:")
        # print(packet)

    def checkAcknowledgementPacket(self, data: bytes) -> bool:
        if len(data) == 6:
            if PacketInterpreter.getTransmissionId(
                    data) == self.transmission_id and PacketInterpreter.getSequenceNumber(data) == self.sequence_number:
                return True
        return False

    def handleAcknowledgementPacket(self):
        try:
            data, addr = self.socket.recvfrom(self.buffer_size)
            if not self.checkAcknowledgementPacket(data):
                print("Did not receive valid acknowledgement packet, abort transmission")
                self.socket.close()
                return False
        except socket.timeout:
            print("Did not receive acknowledgement packet in time, abort transmission")
            self.socket.close()
            return False
        return True

    def handleSlidingAcknowledgementPacket(self) -> bool:
        try:
            data, addr = self.socket.recvfrom(self.buffer_size)
            if not self.checkAcknowledgementPacket(data):
                data, addr = self.socket.recvfrom(self.buffer_size)
                temp_packet = PacketInterpreter.getSequenceNumber(data)
                self.send_packet(self.window_buffer.get(temp_packet))
                return False
            else:
                self.window_buffer.clear()
                return True
        except Exception as e:
            print(e)
            print("Did not receive acknowledgement packet in time, abort transmission")
            self.socket.close()
            return True
