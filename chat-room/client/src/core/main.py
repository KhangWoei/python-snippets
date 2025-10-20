from select import epoll, EPOLLIN
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
import signal
import sys
from types import FrameType
from typing import List, Tuple

def main() -> None:
    client: socket = socket(AF_INET, SOCK_STREAM)

    client.connect(("0.0.0.0", 9999))

    def _cleanup(sig: int, frame: FrameType | None):
        print("shutting down..")
        client.shutdown(SHUT_RDWR)
        client.close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, _cleanup)
    signal.signal(signal.SIGINT, _cleanup)
    
    client_descriptors: epoll = epoll()
    client_descriptors.register(sys.stdin.fileno(), EPOLLIN)
    client_descriptors.register(client.fileno(), EPOLLIN)

    while True:
        events: List[Tuple[int, int]] = client_descriptors.poll()

        for file_descriptor, event in events:
            if file_descriptor == sys.stdin.fileno():
                message: str = sys.stdin.readline().strip()
                if message:
                    client.send(message.encode())
            elif file_descriptor == client.fileno():
                data: bytes = client.recv(4096)

                if data:
                    print(data.decode())
                else:
                    _cleanup(0, None)


if __name__ == "__main__":
    main()
