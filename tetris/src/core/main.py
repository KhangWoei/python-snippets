import curses
from .game import Game

def main() -> None:
    game = Game()

    curses.wrapper(game.start)

if __name__ == "__main__":
    main()
