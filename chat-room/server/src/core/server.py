from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from types import TracebackType
from typing import Dict, List, Tuple, Self
from dataclasses import dataclass
from selectors import DefaultSelector, EVENT_READ, SelectorKey
import logging

logger = logging.getLogger(__name__)

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
        logger.info("Cleaning up")

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
        try:
            server: socket = self._socket
            server.listen()
            logger.info(f"Listening on {server.getsockname()}")
            file_descriptors: DefaultSelector = self._selector
            file_descriptors.register(server, EVENT_READ)
            while True:
                logger.info("Polling ...")
                events: List[Tuple[SelectorKey, int]]  = file_descriptors.select(1)

                for key, _ in events:
                    if key.fd == server.fileno():
                        logger.info("Registering client...")
                        new_client:socket 
                        addr: str
                        new_client, addr = server.accept()
                        self._clients[new_client.fileno()] = Client(new_client, addr)

                        file_descriptors.register(new_client, EVENT_READ)
                    else:
                        logger.info("Client data received...")
                        current_client: Client = self._clients[key.fd]
                        data: bytes = current_client.socket.recv(1024)

                        if data:
                            msg: str = f"[{current_client.address}]: {data}"
                            logger.info(msg)
                            self._broadcast(msg)
                        else:
                            logger.info("Un-registering client...")
                            del self._clients[key.fd]
                            file_descriptors.unregister(current_client.socket)
                            current_client.socket.close()
        except KeyboardInterrupt:
            logger.info("Shutting down")
    
    def _broadcast(self, msg:str) -> None:
        encoded_msg = msg.encode()

        for fd, client in self._clients.items():
            client.socket.send(encoded_msg)

