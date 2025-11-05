import dataclasses
from enum import Enum
from json import JSONEncoder, JSONDecoder, dumps, loads
from typing import Any, Dict, Self
import logging

logger = logging.getLogger(__name__)

class MessageType(Enum):
    SERVER = 1
    ROOM = 2
    USER = 3

@dataclasses.dataclass
class Message():
    type: MessageType;
    sender: str;
    recipient: str | None;
    content: str;

    def to_json_string(self) -> str:
        return dumps(self, cls=ExtendedEncoder)

    """ Consider using @classmethod. 
        Unlike @staticmethod, class methods take the class type as it's first input, good candidate for implementing creation or factory patterns or even parsing like this one.
    """
    @classmethod
    def from_json_string(cls, input: str) -> Self:
        data: Dict[str, Any] = loads(input)

        if "type" not in data or "sender" not in data or "content" not in data:
            error: TypeError = TypeError(f"Unable to parse: {input} to {cls}")
            logger.error(error)
            raise error

        data["type"] = MessageType(data["type"])

        return cls(**data)

class ExtendedEncoder(JSONEncoder):
    """ Whenever the encoder hits an unknown datatype, 
        it'll interrogate the default method for 
        answers. The base encoder doesn't know how to serialize dataclasses and enums.
        We can see this in the last case of the iterencode function.
    """
    def default(self, o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            data: Dict[str, Any] = dataclasses.asdict(o)
            return data

        if isinstance(o, Enum):
            return o.value

        return super().default(o)

