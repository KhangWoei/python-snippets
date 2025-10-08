import configuration.configuration as cfg
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
import signal
import sys

class Server():

    def __init__(self, address: str, port: int):
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind((address, port))


    def start_server(self) -> None:
        server = self._socket

        server.listen(5)
        print(f"Listening on {server.getsockname()}")

        client, addr = server.accept()
        
        try:
            while True:
                request = client.recv(1024)
                print(f"Received: {request}")

                client.send("Ping received".encode())
        finally:
            server.close()
            sys.exit(0)

if __name__ == "__main__":
    config = cfg.load()
    print(f"{config.address}:{config.port}")

    server = Server(config.address, config.port)

    server.start_server()
