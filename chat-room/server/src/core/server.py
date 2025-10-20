from socket import socket, AF_INET, SOCK_STREAM
from types import TracebackType
from typing import Dict, List, Tuple, Self
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
        self._epoll: epoll = epoll()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        for client in self._clients.values():
            try:
                client.socket.close()
            except:
                pass
        self._clients.clear()

        try:
            self._epoll.close()
        except:
            pass

        try:
            self._socket.close()
        except:
            pass


    def start_server(self) -> None:
        server: socket = self._socket

        server.listen(5)
        print(f"Listening on {server.getsockname()}")

        file_descriptors: epoll = self._epoll
        file_descriptors.register(server.fileno(), EPOLLIN)

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
                        msg: str = f"[{current_client.address}, {current_client.socket.fileno()}]: {data}"
                        print(msg)
                        self._broadcast(msg)
                    else:
                        print("Un-registering client...")
                        del self._clients[file_descriptor]
                        file_descriptors.unregister(current_client.socket.fileno())
                        current_client.socket.close()
    
    def _broadcast(self, msg:str) -> None:
        encoded_msg = msg.encode()

        for fd, client in self._clients.items():
            client.socket.send(encoded_msg)

