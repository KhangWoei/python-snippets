import curses
from dataclasses import dataclass

class Game:
    _board_height = 20
    _board_width = 10

    _block_height = 2
    _block_width = 4

    def __init__(self, window: curses.window) -> None:
        self._window = window
        self._height, self._width = window.getmaxyx()

        self._start_y = (self._height - (self._board_height * self._block_height) - 2) // 2
        self._start_x = (self._width - (self._board_width * self._block_width) - 2) // 2

        self._board = [[0 for _ in range(self._board_width)] for _ in range(self._board_height)]

        self._game_over = False

    def start(self) -> None:
        self._window.clear()

        while not self._game_over:
            self._draw_board()
    
    def _draw_board(self) -> None:
        window = self._window
        self._draw_border()
        self._draw_cells()

        window.refresh()

    def _draw_border(self) -> None:
        window = self._window

        border_inner_height = (self._board_height + 1) * self._block_height
        border_inner_width = self._board_width * self._block_width

        window.addstr(self._start_y, self._start_x, "+" + "-" * border_inner_width + "+")

        for row in range(0, border_inner_height):
            window.addstr(self._start_y + row, self._start_x, "|")
            window.addstr(self._start_y + row, self._start_x + border_inner_width + 1, "|")

        window.addstr(self._start_y + border_inner_height, self._start_x, "+" + "-" * border_inner_width + "+")

    def _draw_cells(self) -> None:
        window = self._window

        for row_idx, row in enumerate(self._board):
            for col_idx, cell in enumerate(row):
                if cell != 0:
                    cell_y = self._start_y + (row_idx * self._block_height)
                    cell_x = self._start_x + 1 + (col_idx * self._block_width)

                    for h in range(self._block_height):
                        window.addstr(cell_y + h, cell_x, "[" + "x" * (self._block_width - 2) + "]")

def _start(window: curses.window) -> None:
    game = Game(window)

    game.start()

def main() -> None:
    curses.wrapper(_start)

if __name__ == "__main__":
    main()
