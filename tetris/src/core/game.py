from curses import window, curs_set
from .board import Board, Moves
from .block_size import BlockSize
from .border_decorator import BorderDecorator
from time import time

class Game():
    def __init__(self, drop_speed: float = 0.5, block_height: int = 2, block_width: int = 4):
        self._drop_speed = drop_speed
        
        self._block_size = BlockSize(block_height, block_width)

    def start(self, window: window):
        curs_set(0)

        window.clear()

        board: Board = Board(window, self._block_size)
        border: BorderDecorator = BorderDecorator(window, board.window)
        border.render()

        last_drop = time()
        while True:
            board.render()

            if time() - last_drop > self._drop_speed:
                board.move(Moves.DROP)
                last_drop = time()

