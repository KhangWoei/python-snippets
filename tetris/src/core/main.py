import curses

class Game:
    def __init__(self, window: curses.window) -> None:
        self._window = window
        self._height, self._width = window.getmaxyx()

    def start(self) -> None:
        self._window.clear()

        while True:
            self._draw_board()
    
    def _draw_board(self) -> None:
        window = self._window
        self._draw_border()
        window.refresh()

    def _draw_border(self) -> None:
        window = self._window

        window.addstr(0, 0, "+" + "-" * (self._width - 2) + "+")

        for row in range(1, self._height - 2):
            window.addstr(row, 0, "|")
            window.addstr(row, self._width - 1, "|")

        window.addstr(self._height - 2, 0, "+" + "-" * (self._width - 2) + "+")

def _start(window: curses.window) -> None:
    game = Game(window)

    game.start()

def main() -> None:
    curses.wrapper(_start)

if __name__ == "__main__":
    main()
