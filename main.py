import sys
import socket
from Sender import Sender

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 main.py transmission_id file_name port")
        return

    transmission_id = int(sys.argv[1])
    file_path = sys.argv[2]
    port = int(sys.argv[3])

    with open(file_path, "rb") as f:
        sender = Sender(f, socket.gethostbyname(socket.gethostname()), port, 128, transmission_id, 1)
        sender.send()

if __name__ == '__main__':
    main()
