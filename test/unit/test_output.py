from output import stringify # type: ignore


def test_stringify_float():
    # print the number 'with the minimum number of decimal places without losing precision'
    assert stringify(12.345) == "12.345"
    assert stringify(12.3400) == "12.34"
    assert stringify(12.3) == "12.3"
    assert stringify(12.0) == "12"
    assert stringify(0.50) == "0.5"
    assert stringify(0.0) == "0"


def test_stringify_none():
    assert stringify(None) == "nil"


def test_stringify_booleans():
    assert stringify(True) == "true"
    assert stringify(False) == "false"


def test_stringify_others():
    assert stringify("hello world!") == "hello world!"
    assert stringify("5.500") == "5.500"
    assert stringify("") == ""
    assert stringify("True") == "True"
