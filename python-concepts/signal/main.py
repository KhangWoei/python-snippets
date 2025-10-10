from sys import exit
from types import FrameType
from signal import signal, SIGINT, SIGTERM

def main() -> None:
    def on_signal(sig: int, frame: FrameType | None) -> None:
        print(f"Signal: {sig}, Frame: {frame}")

        match sig:
            case _:
                exit()

    signal(SIGINT, on_signal)
    signal(SIGTERM, on_signal)

    print("Waiting for signal...")
    
    while True:
        pass

if __name__ == "__main__":
    main()
