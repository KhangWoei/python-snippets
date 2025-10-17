from curses import window, curs_set, KEY_LEFT, KEY_RIGHT, KEY_DOWN, KEY_UP, newwin

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
        self._score = 0

    def start(self, window: window):
        event_bus = EventBus()
        event_bus.subscribe(GameEvents.GAME_OVER, self._handle_game_over)
        event_bus.subscribe(GameEvents.LINE_CLEARED, self._handle_line_clear)

        curs_set(0)
        window.nodelay(True)

        window.clear()

        board: Board = Board(window, self._block_size, event_bus)
        border: BorderDecorator = BorderDecorator(window, board.window)
        border.render()

        score_window = self._create_score_window(board)

        last_drop = time()
        while not self._game_over:
            board.render()
            self._render_score(score_window)

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

    def _handle_line_clear(self, **kwargs):
        lines: int | None = kwargs.get("lines")

        if lines:
            self._score += (lines * 100)

    def _create_score_window(self, board: Board) -> window:
        _, board_max_x = board.window.getmaxyx()
        board_y, board_x = board.window.getbegyx()

        score_width = 20
        score_height = 5
        score_y = board_y
        score_x = board_x + board_max_x + 2

        return newwin(score_height, score_width, score_y, score_x)

    def _render_score(self, score_window: window) -> None:
        score_window.erase()
        score_window.border()
        score_window.addstr(1, 2, "SCORE")
        score_window.addstr(2, 2, f"{self._score}")
        score_window.refresh()
