from abc import abstractmethod
from content import Content 

class IRenderable:
    @abstractmethod
    def get_content(self) -> Content:
        pass

