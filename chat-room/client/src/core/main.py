import socket 
import signal
import sys

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(("0.0.0.0", 9999))

    def cleanup(sig, frame):
        print("shutting down..")
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    while True:
        message = input()
        client.send(message.encode())

        response = client.recv(4096)
        print(response.decode())

if __name__ == "__main__":
    main()
