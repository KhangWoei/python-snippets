import curses

class Game:
    def __init__(self, window: curses.window) -> None:
        self._window = window
        self._height, self._width = window.getmaxyx()

    def start(self) -> None:
        self._window.clear()

        while True:
            self._draw_board()
    
    def _draw_board(self):
        window = self._window
        self._draw_border()
        window.refresh()

    def _draw_border(self):
        window = self._window

        window.addstr(0, 0, "+" + "-" * (self._width - 2) + "+")

        for row in range(1, self._height - 2):
            window.addstr(row, 0, "|")
            window.addstr(row, self._width - 1, "|")

        window.addstr(self._height - 2, 0, "+" + "-" * (self._width - 2) + "+")

def main(window: curses.window) -> None:
    curses.curs_set(0)
    game = Game(window)

    game.start()

if __name__ == "__main__":
    curses.wrapper(main)
