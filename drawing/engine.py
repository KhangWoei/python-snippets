from dataclasses import dataclass
import os 
import sys

@dataclass
class Region:
    x: int
    y: int

class Engine:
    def __init__(self):
        self._width, self._height = self._get_terminal_size()

        self._clear_screen()

    def _get_terminal_size(self) -> tuple[int, int]:
        try:
            return os.get_terminal_size().columns, os.get_terminal_size().lines
        except:
            return 80, 24

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def clear_region(self, region: Region) -> None:
        for y in range(region.y, region.y + self._height):
            if y < self.height:
                sys.stdout.write(' ' * min(self.width, self.width - region.x))

    def move_cursor(self, x: int, y: int) -> None:
        sys.stdout.write(f'\033[{y + 1};{x + 1}H')

    def _clear_screen(self) -> None:
        sys.stdout.write('\033[2J')
        sys.stdout.write('\033[H')
        sys.stdout.flush()

    def render(self, content: str) -> None:
        sys.stdout.write(content)
        sys.stdout.flush()

