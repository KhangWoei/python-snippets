from enum import Enum
from dataclasses import dataclass

class ContentType(Enum):
    UNKNOWN = 0
    INPUT_PROMPT = 1
    MESSAGE = 2
    COMMAND_LIST = 3

@dataclass
class Content:
    content: str
    content_type: ContentType
