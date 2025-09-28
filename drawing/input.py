from content import Content, ContentType
from renderable import IRenderable

class Input(IRenderable):
    
    def __init__(self, user: str, room: str) -> None:
        self._user = user
        self._room = room
        super().__init__

    def get_content(self) -> Content:
        content = f"{self._user}@{self._room}:"
        return Content(content, ContentType.INPUT_PROMPT)

