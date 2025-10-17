from enum import Enum
from typing import Callable, Dict, List, Any

class GameEvents(Enum):
    GAME_OVER = 1
    LINE_CLEARED = 2

class BoardEvents(Enum):
    ROTATE = 1,
    LEFT = 2,
    RIGHT = 3,
    DROP = 4

class EventBus:
    def __init__(self) -> None:
        self._listeners: Dict[GameEvents | BoardEvents, List[Callable]] = {}

    def subscribe(self, event: GameEvents | BoardEvents, callback: Callable) -> None:
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def emit(self, event: GameEvents | BoardEvents, **data: Any) -> None:
        if event in self._listeners:
            for callback in self._listeners[event]:
                callback(**data)

