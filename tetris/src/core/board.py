from curses import window, newwin
from .block_size import BlockSize

class Board():
    _board_height = 20
    _board_width = 10

    def __init__(self, window: window, block_size: BlockSize) -> None:
        self._block_size = block_size
        max_height, max_width = window.getmaxyx()

        mapped_height = self._board_height * block_size.height
        mapped_width = self._board_width * block_size.width

        start_y = (max_height - (mapped_height)) // 2
        start_x = (max_width - (mapped_width)) // 2

        self._window = newwin(mapped_height + 1, mapped_width, start_y, start_x)
        self._board = [[0 for _ in range(self._board_width)] for _ in range(self._board_height)]

    @property
    def window(self) -> window:
        return self._window

    def render(self) -> None:
        self._render_cells()
        self._window.refresh()

    def _render_cells(self) -> None:
        for row_index, row in enumerate(self._board):
            for col_index, cell in enumerate(row):
                if cell != 0:
                    cell_y = row_index * self._block_size.height
                    cell_x = col_index * self._block_size.width

                    for height in range(self._block_size.height):
                        self.window.addstr(cell_y + height, cell_x, "[" + "x" * (self._block_size.width - 2) + "]")

