from socket import socket, AF_INET, SOCK_STREAM
import sys
from typing import Dict, List, Tuple
from select import epoll, EPOLLIN
from dataclasses import dataclass

@dataclass
class Client():
    socket: socket
    address: str

class Server():

    def __init__(self, address: str, port: int):
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind((address, port))
        self._clients: Dict[int, Client] = {}


    def start_server(self) -> None:
        server = self._socket

        server.listen(5)
        print(f"Listening on {server.getsockname()}")

        file_descriptors: epoll = epoll()
        file_descriptors.register(server.fileno(), EPOLLIN)

        try:
            while True:
                print("Polling ...")
                events: List[Tuple[int, int]]  = file_descriptors.poll()

                for file_descriptor, event in events:
                    if file_descriptor == server.fileno():
                        print("Registering client...")
                        new_client:socket 
                        addr: str
                        new_client, addr = server.accept()
                        self._clients[new_client.fileno()] = Client(new_client, addr)
                        print(self._clients)                       

                        file_descriptors.register(new_client.fileno(), EPOLLIN)
                    else:
                        print("Client data received...")
                        current_client: Client = self._clients[file_descriptor]
                        data: bytes = current_client.socket.recv(1024)

                        if data:
                            print(f"[{current_client.address}, {current_client.socket.fileno()}]: {data}")
                            current_client.socket.send("Received".encode())
                        
        finally:
            server.close()
            sys.exit(0)

