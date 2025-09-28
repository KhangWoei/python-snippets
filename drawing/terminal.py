from dataclasses import dataclass
from engine import Engine, Region
from renderable import IRenderable 
from content import ContentType

class Terminal:
    def __init__(self, engine: Engine):
        self._engine = engine
        self._create_layout()

    def _create_layout(self):
        height = self._engine.height
        
        self._message_region = Region(0, 0)
        self._input_region = Region(0, height - 1)
    
    def render(self, render_object: IRenderable) -> None:
        content = render_object.get_content() 

        match content.content_type:
            case ContentType.INPUT_PROMPT:
                self._engine.move_cursor(self._input_region.x, self._input_region.y)
                self._engine.render(content.content)
                self._input_region.x = len(content.content) + 2
                return
            case ContentType.MESSAGE:
                self._engine.move_cursor(self._message_region.x, self._message_region.y)
                self._engine.render(content.content)
                self._engine.move_cursor(self._input_region.x, self._input_region.y)
                return
            case _:
                # raise UnsupportedContentType(content.content_type)
                raise Exception(f"Unsupported content type: {content.content_type}")
