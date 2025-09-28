from content import Content, ContentType
from renderable import IRenderable

class Message(IRenderable):

    def __init__(self, sender: str, room: str, message: str) -> None:
        self._sender = sender
        self._room = room 
        self._message = message 

        super().__init__

    def get_content(self) -> Content:
        content = f"{self._sender}@{self._room}:"
        return Content(content, ContentType.MESSAGE)

