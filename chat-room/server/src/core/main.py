import configuration.configuration as cfg
from .server import Server

def main() -> None:
    config = cfg.load()
    print(f"{config.address}:{config.port}")

    server = Server(config.address, config.port)

    server.start_server()

if __name__ == "__main__":
    main()
