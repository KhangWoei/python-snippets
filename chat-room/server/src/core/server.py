from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from types import TracebackType
from typing import Dict, List, Tuple, Self
from dataclasses import dataclass
from selectors import DefaultSelector, EVENT_READ, SelectorKey

@dataclass
class Client():
    socket: socket
    address: str

class Server():

    def __init__(self, address: str, port: int) -> None:
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind((address, port))
        self._clients: Dict[int, Client] = {}
        self._selector: DefaultSelector = DefaultSelector()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        print("Cleaning up")

        for client in self._clients.values():
            try:
                client.socket.shutdown(SHUT_RDWR);
                client.socket.close()
            except:
                pass
        self._clients.clear()

        try:
            self._selector.close()
            self._socket.close()
        except:
            pass


    def start_server(self) -> None:
        server: socket = self._socket

        server.listen(5)
        print(f"Listening on {server.getsockname()}")
        file_descriptors: DefaultSelector = self._selector
        file_descriptors.register(server, EVENT_READ)

        while True:
            print("Polling ...??")
            events: List[Tuple[SelectorKey, int]]  = file_descriptors.select()

            for key, _ in events:
                if key.fd == server.fileno():
                    print("Registering client...")
                    new_client:socket 
                    addr: str
                    new_client, addr = server.accept()
                    self._clients[new_client.fileno()] = Client(new_client, addr)

                    file_descriptors.register(new_client, EVENT_READ)
                else:
                    print("Client data received...")
                    current_client: Client = self._clients[key.fd]
                    data: bytes = current_client.socket.recv(1024)

                    if data:
                        msg: str = f"[{current_client.address}]: {data}"
                        print(msg)
                        self._broadcast(msg)
                    else:
                        print("Un-registering client...")
                        del self._clients[key.fd]
                        file_descriptors.unregister(current_client.socket)
                        current_client.socket.close()
    
    def _broadcast(self, msg:str) -> None:
        encoded_msg = msg.encode()

        for fd, client in self._clients.items():
            client.socket.send(encoded_msg)

