from signal import signal, SIGTERM, SIGINT
from sys import exit
from select import epoll, EPOLLIN
from socket import socket, AF_INET, SOCK_DGRAM
from types import FrameType
from typing import Dict, List, Tuple

def main() -> None:
    socket1: socket = socket(AF_INET, SOCK_DGRAM)
    socket1.bind(("0.0.0.0", 9999))

    socket2: socket = socket(AF_INET, SOCK_DGRAM)
    socket2.bind(("0.0.0.0", 9998))

    def cleanup(sig: int, frame: FrameType | None):
        socket1.close()
        socket2.close()
        exit(0)

    signal(SIGTERM, cleanup)
    signal(SIGINT, cleanup)

    socket_map: Dict[int,socket] = {
        socket1.fileno(): socket1,
        socket2.fileno(): socket2
    }
    polled_sockets: epoll = epoll()
    polled_sockets.register(socket1.fileno(), EPOLLIN)
    polled_sockets.register(socket2.fileno(), EPOLLIN)

    while True:
        print("Polling...")
        events: List[Tuple[int, int]] = polled_sockets.poll()
        
        for fd, event in events:
            
            if event == EPOLLIN:    
                current_socket = socket_map[fd]
                data = current_socket.recv(1024)

                if data:
                    print(f"{current_socket.getsockname()}: {data}")
                else:
                    print(f"{current_socket.getsockname()} : disconnected")


if __name__ == "__main__":
    main()
