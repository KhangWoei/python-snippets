import os 
import sys

class Engine:
    def __init__(self):
        self.width, self.height = self._get_terminal_size()

        self._clear_screen()

    def _get_terminal_size(self) -> tuple[int, int]:
        try:
            return os.get_terminal_size().columns, os.get_terminal_size().lines
        except:
            return 80, 24

    def _clear_screen(self) -> None:
        sys.stdout.write('\033[2J')
        sys.stdout.write('\033[H')
        sys.stdout.flush()

    def render(self, content: str) -> None:
        sys.stdout.write(content)
        sys.stdout.flush()

