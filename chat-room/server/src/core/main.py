import configuration.configuration as cfg
from .server import Server

def main() -> None:
    config = cfg.load()
    print(f"{config.address}:{config.port}")

    with Server(config.address, config.port) as server:
        server.start_server()

if __name__ == "__main__":
    main()
