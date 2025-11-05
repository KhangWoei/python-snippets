from kchat_shared.message import Message, MessageType

def test_roundtrip():
    expected: Message = Message(MessageType.SERVER, "John Doe", None, "Hello World")

    encoded_message: str = expected.to_json_string()

    actual: Message = Message.from_json_string(encoded_message)
        
    assert _is_equal(actual, expected)

def _is_equal(actual: Message, expected: Message) -> bool:
    return  (
        actual.type == expected.type and
        actual.sender == expected.sender and 
        actual.recipient == expected.recipient and
        actual.content == expected.content
    )

