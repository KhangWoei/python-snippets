from signal import signal, SIGTERM, SIGINT
from sys import exit
from select import select
from socket import socket, AF_INET, SOCK_DGRAM
from types import FrameType
from typing import List

def main() -> None:
    socket1 = socket(AF_INET, SOCK_DGRAM)
    socket1.bind(("0.0.0.0", 9999))

    socket2 = socket(AF_INET, SOCK_DGRAM)
    socket2.bind(("0.0.0.0", 9998))

    def cleanup(sig: int, frame: FrameType | None):
        socket1.close()
        socket2.close()
        exit(0)

    signal(SIGTERM, cleanup)
    signal(SIGINT, cleanup)

    sockets: List[socket] = [socket1, socket2]

    while True:
        readers, _, _= select(sockets, [], [])
        
        for reader in readers:
            data = reader.recv(1024)

            if data:
                print(f"{reader.getsockname()}: {data}")
            else:
                print(f"{reader.getsockname()} : disconnected")

if __name__ == "__main__":
    main()
