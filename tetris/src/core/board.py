from curses import window, newwin
from .block_size import BlockSize
from typing import List
from .piece import Piece, RandomPieceFactory
from enum import Enum

class Moves(Enum):
    ROTATE = 1
    LEFT = 2
    RIGHT = 3
    DROP = 4

class Board():
    _board_height = 20
    _board_width = 10

    def __init__(self, parent_window: window, block_size: BlockSize) -> None:
        max_height, max_width = parent_window.getmaxyx()
        mapped_height: int = self._board_height * block_size.height
        mapped_width: int = self._board_width * block_size.width
        start_y: int = (max_height - (mapped_height)) // 2
        start_x: int = (max_width - (mapped_width)) // 2
        self._window: window = newwin(mapped_height + 1, mapped_width, start_y, start_x)
        
        self._block_size: BlockSize = block_size

        self._board: List[List[int]] = [[0 for _ in range(self._board_width)] for _ in range(self._board_height)]
        self._current_piece: Piece = RandomPieceFactory.create(0, self._board_width // 2)

    @property
    def window(self) -> window:
        return self._window

    def move(self, move: Moves) -> None:
        match move:
            case Moves.ROTATE:
                pass
            case Moves.LEFT:
                self._current_piece.x -= 1
                pass
            case Moves.RIGHT:
                self._current_piece.x += 1
                pass
            case Moves.DROP:
                self._current_piece.y += 1
                pass
            case _:
                pass
                

    def render(self) -> None:
        self._window.erase()
        self._render_piece()
        self._render_cells()
        self._window.refresh()
    
    def _render_piece(self) -> None:
        for y, row in enumerate(self._current_piece.shape):
            for x, cell in enumerate(row):
                if cell != 0:
                    cell_y = (self._current_piece.y + y) * self._block_size.height
                    cell_x = (self._current_piece.x + x) * self._block_size.width

                    for height in range(self._block_size.height):
                        self.window.addstr(cell_y + height, cell_x, "[" + "x" * (self._block_size.width - 2) + "]")

    def _render_cells(self) -> None:
        for y, row in enumerate(self._board):
            for x, cell in enumerate(row):
                if cell != 0:
                    cell_y = y * self._block_size.height
                    cell_x = x * self._block_size.width

                    for height in range(self._block_size.height):
                        self.window.addstr(cell_y + height, cell_x, "[" + "x" * (self._block_size.width - 2) + "]")

