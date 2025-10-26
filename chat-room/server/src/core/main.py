import configuration.configuration as cfg
from .server import Server
from message import message

def main() -> None:
    message.test()

    config = cfg.load()
    print(f"{config.address}:{config.port}")

    with Server(config.address, config.port) as server:
        server.start_server()

if __name__ == "__main__":
    main()
