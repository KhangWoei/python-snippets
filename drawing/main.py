from engine import Engine 
from terminal import Terminal
from input import Input
from message import Message

if __name__ == "__main__":
    engine = Engine()
    terminal = Terminal(engine)
    
    input_render = Input("john", "room1")

    terminal.render(input_render)
    while True:
        user_input = input()

        message = Message("sender", "room1", user_input)

        terminal.render(message)

