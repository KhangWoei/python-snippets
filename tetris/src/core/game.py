from curses import window, curs_set, KEY_LEFT, KEY_RIGHT, KEY_DOWN, KEY_UP

from .event_bus import EventBus, GameEvents
from .board import Board, Moves
from .block_size import BlockSize
from .border_decorator import BorderDecorator
from time import time

class Game():
    def __init__(self, drop_speed: float = 0.5, block_height: int = 2, block_width: int = 4):
        self._drop_speed = drop_speed
        
        self._block_size = BlockSize(block_height, block_width)
        self._game_over = False

    def start(self, window: window):
        event_bus = EventBus()
        event_bus.subscribe(GameEvents.GAME_OVER, self._handle_game_over)

        curs_set(0)
        window.nodelay(True)

        window.clear()

        board: Board = Board(window, self._block_size, event_bus)
        border: BorderDecorator = BorderDecorator(window, board.window)
        border.render()

        last_drop = time()
        while not self._game_over:
            board.render()

            if time() - last_drop > self._drop_speed:
                board.move(Moves.DROP)
                last_drop = time()

            key = window.getch()
            if key == ord('q'):
                break
            elif key == KEY_LEFT:
                board.move(Moves.LEFT)
            elif key == KEY_RIGHT:
                board.move(Moves.RIGHT)
            elif key == KEY_DOWN:
                board.move(Moves.DROP)
                last_drop = time()
            elif key == KEY_UP:
                board.move(Moves.ROTATE)

    def _handle_game_over(self, **kwargs):
        self._game_over = True
