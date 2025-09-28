import configuration.configuration as cfg
from socket import socket, AF_INET, SOCK_STREAM
from contextlib import contextmanager

class Server():
    def __init__(self, address: str, port: int):
        self._address = address
        self._port = port

    @contextmanager
    def start_server(self):
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((self._address, self._port))
        server.listen(5)

        try:
            yield server
        finally:
            server.close()

class Client():
    pass

if __name__ == "__main__":
    config = cfg.load()
    print(f"{config.address}:{config.port}")

    with Server(config.address, config.port).start_server() as server:
        print(f"Listening on {server.getsockname()}")

        while True:
            client, addr = server.accept()
            print(f"Accepted connection from {addr}")
            request = client.recv(1024)
            print(f"Received: {request}")

            client.send("Ping received".encode())
            client.close()
        
