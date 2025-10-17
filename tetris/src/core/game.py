from curses import window, curs_set, KEY_LEFT, KEY_RIGHT, KEY_DOWN, KEY_UP, newwin
from .event_bus import EventBus, GameEvents, BoardEvents
from .board import Board, Moves
from .block_size import BlockSize
from .border_decorator import BorderDecorator
from time import time

class Game():
    def __init__(self, drop_speed: float = 0.5, block_height: int = 2, block_width: int = 4):
        self._drop_speed: float = drop_speed

        self._block_size: BlockSize = BlockSize(block_height, block_width)
        self._game_over: bool = False
        self._score: int = 0

    def start(self, game_window: window):
        event_bus: EventBus = EventBus()
        event_bus.subscribe(GameEvents.GAME_OVER, self._handle_game_over)
        event_bus.subscribe(GameEvents.LINE_CLEARED, self._handle_line_clear)

        curs_set(0)
        game_window.nodelay(True)
        game_window.clear()

        board: Board = Board(game_window, self._block_size, event_bus)
        border: BorderDecorator = BorderDecorator(game_window, board.window)
        border.render()

        score_window: window = self._create_score_window(board)

        last_drop: float = time()
        while not self._game_over:
            board.render()
            self._render_score(score_window)

            if time() - last_drop > self._drop_speed:
                event_bus.emit(BoardEvents.DROP)
                last_drop = time()

            key: int= game_window.getch()
            if key == ord('q'):
                break
            elif key == KEY_UP:
                event_bus.emit(BoardEvents.ROTATE)
            elif key == KEY_LEFT:
                event_bus.emit(BoardEvents.LEFT)
            elif key == KEY_RIGHT:
                event_bus.emit(BoardEvents.RIGHT)
            elif key == KEY_DOWN:
                event_bus.emit(BoardEvents.DROP)
                last_drop = time()

    def _handle_game_over(self, **kwargs):
        self._game_over = True

    def _handle_line_clear(self, **kwargs):
        lines: int | None = kwargs.get("lines")

        if lines:
            self._score += (lines * 100)

    def _create_score_window(self, board: Board) -> window:
        _, board_max_x = board.window.getmaxyx()
        board_y, board_x = board.window.getbegyx()

        score_width: int = 20
        score_height: int = 5
        score_y: int = board_y
        score_x: int= board_x + board_max_x + 2

        return newwin(score_height, score_width, score_y, score_x)

    def _render_score(self, score_window: window) -> None:
        score_window.erase()
        score_window.border()
        score_window.addstr(1, 2, "SCORE")
        score_window.addstr(2, 2, f"{self._score}")
        score_window.refresh()
