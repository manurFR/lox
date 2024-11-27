from parsing import Literal, Parser  # type: ignore
from scanning import Token  # type: ignore

TOKENS = [Token("NUMBER", "2", 2.0), 
          Token("STAR", "*", None), 
          Token("NUMBER", "3", 3.0),
          Token("EOF", "", None)]
LAST = len(TOKENS) - 1


def test_Literal_repr():
    assert repr(Literal(True)) == "true"
    assert repr(Literal(False)) == "false"
    assert repr(Literal(None)) == "nil"
    assert repr(Literal("test")) == "test"
    assert repr(Literal(12.34)) == "12.34"


def test_Parser_peek():
    p = Parser(TOKENS)
    assert p.peek() == "NUMBER"
    p.current = 1
    assert p.peek() == "STAR"


def test_Parser_is_at_end():
    p = Parser(TOKENS)
    assert p.is_at_end() is False
    p.current = LAST
    assert p.is_at_end() is True


def test_Parser_advance():
    p = Parser(TOKENS)
    p.current = LAST - 1
    p.advance()
    assert p.current == LAST
    p.advance()
    assert p.current == LAST


def test_Parser_match():
    p = Parser(TOKENS)
    assert p.match("STAR") is False
    assert p.match("NUMBER") is True
    # even though the last token is EOF, a match on it always returns False
    p.current = LAST
    assert p.match("EOF") is False