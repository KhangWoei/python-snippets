from socket import socket, AF_INET, SOCK_STREAM
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

