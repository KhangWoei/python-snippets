from curses import window

class BorderDecorator:

    def __init__(self, parent_window: window, child_window: window) -> None:
        self._parent_window = parent_window
        self._child_window = child_window

    def render(self) -> None:
        start_y, start_x = self._child_window.getbegyx()
        height, width = self._child_window.getmaxyx()

        self._parent_window.addstr(start_y - 1, start_x - 1, "+" + "-" * width + "+")

        for row in range(height):
            self._parent_window.addstr(start_y + row, start_x - 1, "|")
            self._parent_window.addstr(start_y + row, start_x + width, "|")

        self._parent_window.addstr(start_y + height, start_x - 1, "+" + "-" * width + "+")

        self._parent_window.refresh()
