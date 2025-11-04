import dataclasses
from enum import Enum
from json import JSONEncoder, JSONDecoder
from typing import Any, Dict

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

class ExtendedEncoder(JSONEncoder):
    """ Whenever the encoder hits an unknown datatype, 
        it'll interrogate the default method for 
        answers. The base encoder doesn't know how to serialize dataclasses and enums.
        We can see this in the last case of the iterencode function.
    """
    def default(self, o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            data: Dict[str, Any] = dataclasses.asdict(o)
            data["__type__"] = o.__class__.__name__
            return data

        if isinstance(o, Enum):
            return o.name

        return super().default(o)

class ExtendedDecoder(JSONDecoder):

    _type_map: Dict[str, type] = {
        Message.__name__: Message
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(object_hook=self._hook, *args, **kwargs)

    def _hook(self, dct: Dict[str, Any]) -> Any:
        type_attribute: str | None = dct.pop("__type__") if "__type__" in dct else None

        if type_attribute is not None:
            decoded_type: object | None = self._type_map.get(type_attribute)

            if decoded_type is not None:
                return decoded_type(**dct)
        
        return dct

