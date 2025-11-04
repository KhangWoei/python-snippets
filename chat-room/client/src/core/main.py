from .client import Client

def main() -> None:
    with Client() as client:
        client.connect("localhost", 9999)

if __name__ == "__main__":
    main()
