from message import message
from json import dumps, loads

def test_roundtrip():
    expected: message.Message = message.Message(message.MessageType.SERVER, "John Doe", None, "Hello World")

    encdoded: str = dumps(expected, cls=message.ExtendedEncoder)

    actual: message.Message = loads(encdoded, cls=message.ExtendedDecoder)
        
    assert _is_equal(actual, expected)

def _is_equal(actual: message.Message, expected: message.Message) -> bool:
    return  (
        actual.type == expected.type and
        actual.sender == expected.sender and 
        actual.recipient == expected.recipient and
        actual.content == expected.content
    )
