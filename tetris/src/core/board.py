from curses import window, newwin
from .block_size import BlockSize

class Board():
    _board_height = 20
    _board_width = 10

    def __init__(self, window: window, block_size: BlockSize) -> None:
        max_height, max_width = window.getmaxyx()
        
        mapped_height = self._board_height * block_size.height
        mapped_width = self._board_width * block_size.width
        
        start_y = (max_height - (mapped_height)) // 2
        start_x = (max_width - (max_width)) // 2

        self._window = newwin(mapped_height, mapped_width, start_y, start_x)
        pass
    
    @property
    def window(self) -> window:
        return self._window

    def render(self) -> None:
        pass
