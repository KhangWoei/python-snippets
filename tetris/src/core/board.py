from curses import window, newwin
from .block_size import BlockSize
from typing import List, Callable, Optional
from .piece import Piece, RandomPieceFactory
from .event_bus import EventBus, GameEvents
from enum import Enum

class Moves(Enum):
    ROTATE = 1
    LEFT = 2
    RIGHT = 3
    DROP = 4

class Board():
    _board_height = 20
    _board_width = 10

    def __init__(self, parent_window: window, block_size: BlockSize, event_bus: EventBus) -> None:
        max_height, max_width = parent_window.getmaxyx()
        mapped_height: int = self._board_height * block_size.height
        mapped_width: int = self._board_width * block_size.width
        start_y: int = (max_height - (mapped_height)) // 2
        start_x: int = (max_width - (mapped_width)) // 2
        self._window: window = newwin(mapped_height + 1, mapped_width, start_y, start_x)

        self._block_size: BlockSize = block_size
        self._event_bus: EventBus = event_bus

        self._board: List[List[int]] = [[0 for _ in range(self._board_width)] for _ in range(self._board_height)]
        self._spawn_new_piece()

    @property
    def window(self) -> window:
        return self._window

    def move(self, move: Moves) -> None:
        match move:
            case Moves.ROTATE:
                self._current_piece.rotate_clockwise()
                if self._would_collide(self._current_piece):
                    self._current_piece.rotate_counter_clockwise()
            case Moves.LEFT:
                if not self._would_collide(self._current_piece, offset_x=-1):
                    self._current_piece.x -= 1
            case Moves.RIGHT:
                if not self._would_collide(self._current_piece, offset_x=-1):
                    self._current_piece.x += 1
            case Moves.DROP:
                if not self._would_collide(self._current_piece, offset_y=1):
                    self._current_piece.y += 1
                else:
                    self._lock_piece()
                    self._spawn_new_piece()

            case _:
                pass

    def _would_collide(self, piece: Piece, offset_y: int = 0, offset_x: int = 0) -> bool:
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell != 0:
                    new_y = piece.y + y + offset_y
                    new_x = piece.x + x + offset_x

                    if (new_x < 0 
                        or new_x >= self._board_width 
                        or new_y < 0 
                        or new_y >= self._board_height 
                        or self._board[new_y][new_x] != 0):
                        return True
        
        return False

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

    def _lock_piece(self) -> None:
        for y, row in enumerate(self._current_piece.shape):
            for x, cell in enumerate(row):
                if cell != 0:
                    board_y = self._current_piece.y + y
                    board_x = self._current_piece.x + x

                    if 0 <= board_y < self._board_height and 0 <= board_x < self._board_width:
                        self._board[board_y][board_x] = 1

        self._clear()

    def _clear(self) -> None:
        lines_cleared = 0

        y = self._board_height - 1
        while y >= 0:
            if all(self._board[y]):
                del self._board[y]
                self._board.insert(0, [0 for _ in range(self._board_width)])
                lines_cleared += 1
            else:
                y -= 1

        if lines_cleared > 0:
            self._event_bus.emit(GameEvents.LINE_CLEARED, lines=lines_cleared)

    def _spawn_new_piece(self) -> None:
        self._current_piece = RandomPieceFactory.create(y=0, x=self._board_width // 2)

        if self._would_collide(self._current_piece):
            self._event_bus.emit(GameEvents.GAME_OVER)

