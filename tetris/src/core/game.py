from curses import window, newwin
from dataclasses import dataclass
from .board import Board
from .block_size import BlockSize

class Game():

    def __init__(self, drop_speed: float = 0.5, block_height: int = 2, block_width: int = 4):
        self._drop_speed = drop_speed
        
        self._block_size = BlockSize(block_height, block_width)

    def start(self, window: window):
        window.clear()

        board = Board(window, self._block_size)
        while True:

            pass

