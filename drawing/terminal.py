from engine import Engine
from renderable import IRenderable 
from content import ContentType

class Terminal:
    def __init__(self, engine: Engine):
        self._engine = engine
    
    def render(self, render_object: IRenderable) -> None:
        content = render_object.get_content() 

        match content.content_type:
            case ContentType.INPUT_PROMPT:
                self._engine.render(content.content)
            case ContentType.MESSAGE:
                self._engine.render(content.content)
            case _:
                # raise UnsupportedContentType(content.content_type)
                raise Exception(f"Unsupported content type: {content.content_type}")
