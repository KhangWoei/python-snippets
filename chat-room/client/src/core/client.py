from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from threading import Thread
from types import TracebackType
from typing import Self

class Client():

    def __init__(self) -> None:
        self._socket: socket = socket(AF_INET, SOCK_STREAM)
        self._running: bool = False

    def connect(self, address: str, port: int) -> None:
        self._socket.connect((address, port))
        self._running = True

        receiver = Thread(target = self._receive_loop, daemon=True)
        receiver.start()

        self._send_loop()

    def _receive_loop(self) -> None:
        while self._running:
            data: bytes = self._socket.recv(4096)

            if data:
                print(f"\r{data.decode()}")
                print("> ", end="", flush=True)
            else:
                self.disconnect()
 
    def _send_loop(self) -> None:
        try:
            while self._running:
                message: str = input("> ")
                self._socket.send((message).encode())
        except (KeyboardInterrupt):
            self.disconnect()

    def disconnect(self) -> None:
        self._running = False
        self._socket.shutdown(SHUT_RDWR)
        self._socket.close()
