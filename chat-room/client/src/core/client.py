from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from threading import Thread, Event
from types import TracebackType
from typing import Self

class Client():

    def __init__(self) -> None:
        self._socket: socket = socket(AF_INET, SOCK_STREAM)
        self._running: Event = Event()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        print("Cleaning up")
        try:
            self._running.clear()
            self._socket.shutdown(SHUT_RDWR)
        except OSError:
            pass
        finally:
            self._socket.close()

    def connect(self, address: str, port: int) -> None:
        try:
            self._socket.connect((address, port))
            self._running.set()

            receiver = Thread(target = self._receive_loop, daemon=True)
            receiver.start()
            
            self._send_loop()
        except KeyboardInterrupt:
            print("Disconnecting")
        except ConnectionRefusedError:
            print(f"Failed to connect to {address}:{port}")
        except OSError as e:
            print(e)

    def _receive_loop(self) -> None:
        while self._running:
            data: bytes = self._socket.recv(4096)

            if data:
                print(f"\r{data.decode()}")
                print("> ", end="", flush=True)
            else:
                break
 
    def _send_loop(self) -> None:
        while self._running:
            message: str = input("> ")
            self._socket.send((message).encode())

