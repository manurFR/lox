import pytest
import re
from parsing import Literal, Grouping, Parser, ParserError  # type: ignore
from scanning import Token  # type: ignore


def _text2tokens(text):
    p = re.compile(r'(\w+) (".*"|.*) (null|.+)')
    tokens = []
    for line in text.strip().split("\n"):
        if (match := p.match(line.strip())):
            toktype, lexeme, literal = match.groups()
            if toktype == "NUMBER":
                literal = float(literal)
            tokens.append(Token(toktype, lexeme, literal))
    tokens.append(Token("EOF", "", None))
    return tokens


TOKENS = _text2tokens("""
                      NUMBER "2" 2.0
                      STAR * null
                      NUMBER "3.14" 3.14
                      """)
LAST = len(TOKENS) - 1


def test_Literal_repr():
    assert repr(Literal(True)) == "true"
    assert repr(Literal(False)) == "false"
    assert repr(Literal(None)) == "nil"
    assert repr(Literal("test")) == "test"
    assert repr(Literal(12.34)) == "12.34"


def test_Grouping_repr():
    assert repr(Grouping(Literal(5.5))) == "(group 5.5)"
    assert repr(Grouping(Literal(False))) == "(group false)"


def test_Parser_primary():
    p = Parser(TOKENS)
    assert p.primary() == Literal(2.0)
    assert Parser([Token("FALSE", "false", None)]).primary() == Literal(False)
    assert Parser([Token("TRUE", "true", None)]).primary() == Literal(True)
    assert Parser([Token("NIL", "nil", None)]).primary() == Literal(None)
    assert Parser([Token("STRING", '"test"', "test")]).primary() == Literal("test")

    grouping_tokens = _text2tokens("""LEFT_PAREN ( null
                                      NUMBER "3.14" 3.14
                                      RIGHT_PAREN ) null""")
    assert Parser(grouping_tokens).primary() == Grouping(Literal(3.14))


def test_Parser_primary_with_unterminated_parentheses():
    p = Parser(_text2tokens("""LEFT_PAREN ( null
                               STRING "fail" fail"""))
    with pytest.raises(ParserError) as ex:
        p.primary()
        assert False  # we should never arrive here
    assert ex.value.args[1] == "Expected ')' after expression."


def test_Parser_peek():
    p = Parser(TOKENS)
    assert p.peek() == "NUMBER"
    p.current = 1
    assert p.peek() == "STAR"


def test_Parser_previous_literal():
    p = Parser(TOKENS)
    p.advance()
    p.advance()
    assert p.peek() == "NUMBER"
    p.advance()
    assert p.previous_literal() == 3.14


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
