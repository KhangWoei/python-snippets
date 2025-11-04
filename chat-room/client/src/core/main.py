from .client import Client

def main() -> None:
    client = Client()
    client.connect("localhost", 9999)

if __name__ == "__main__":
    main()
