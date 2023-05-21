import sys
import socket
from Sender import Sender

def main():
    if len(sys.argv) != 6:
        print("Usage: <transmission_id> <ip> <port> <file_name> <packet_size>")
        return

    transmission_id = int(sys.argv[1])
    ip = sys.argv[2]
    port = int(sys.argv[3])
    file_path = sys.argv[4]
    packet_size = int(sys.argv[5])


    with open(file_path, "rb") as f:
        sender = Sender(f, socket.gethostbyname(ip), port, packet_size, transmission_id, 1)
        sender.send()

if __name__ == '__main__':
    main()
