import configuration.configuration as cfg
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
import signal
import sys

class Server():
    def __init__(self, address: str, port: int):
        self._address = address
        self._port = port

    def start_server(self) -> socket:
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((self._address, self._port))
        server.listen(5)

        return server


if __name__ == "__main__":
    config = cfg.load()
    print(f"{config.address}:{config.port}")

    server = Server(config.address, config.port).start_server()

    print(f"Listening on {server.getsockname()}")
    
    def cleanup(sig, frame):
        print("shutting down..")
        server.shutdown(SHUT_RDWR)
        server.close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    client, addr = server.accept()
    print(f"Accepted connection from {addr}")
    
    try:
        while True:
            request = client.recv(1024)
            print(f"Received: {request}")

            client.send("Ping received".encode())
    except ConnectionResetError:
        print("client shutdown received")
    finally
        server.close()
        sys.exit(0)
