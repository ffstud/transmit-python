import sys
import socket
from Sender import Sender

def main():
    operating_mode = 0
    if len(sys.argv) > 1:
        operating_mode = int(sys.argv[1])

    if operating_mode == 0 and len(sys.argv) != 7:
        print("Usage: <operating_mode> <transmission_id> <ip> <target_port> <file_name> <packet_size>")
        return
    elif operating_mode == 1 and len(sys.argv) != 8:
        print("Usage: <operating_mode> <transmission_id> <ip> <target_port> <file_name> <packet_size> <ack_port>")
        return
    elif operating_mode == 2 and len(sys.argv) != 9:
        print("Usage: <operating_mode> <transmission_id> <ip> <target_port> <file_name> <packet_size> <ack_port> <window_size>")
        return

    transmission_id = int(sys.argv[2])
    ip = sys.argv[3]
    port = int(sys.argv[4])
    file_path = sys.argv[5]
    packet_size = int(sys.argv[6])
    try:
        ack_port = int(sys.argv[7])
    except IndexError:
        ack_port = -1

    try:
        window_size = int(sys.argv[8])
    except IndexError:
        window_size = -1


    sender = Sender(file_path, socket.gethostbyname(ip), port, packet_size, transmission_id, ack_port, operating_mode, window_size)
    sender.send()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated by user")
        sys.exit(0)

