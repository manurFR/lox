import pytest
import re
from parsing import Binary, Unary, Literal, Grouping, Parser, ParserError
from scanning import Token
from syntax import Assign, Call, Logical, Super, Variable
from tokens import AND, DIVISE, LESS_EQUAL, MINUS, NOT_EQUAL, OR, PLUS

TOKEN_PATTERN = re.compile(r'(\w+) (".*"|.*) (null|.+)')


def _parse_token(line):
    if match := TOKEN_PATTERN.match(line.strip()):
        toktype, lexeme, literal = match.groups()
        if toktype == "NUMBER":
            literal = float(literal)
        if literal == "null":
            literal = None
        return Token(toktype, lexeme, literal, 1)
    raise ValueError


def _text2tokens(text):
    tokens = []
    for line in text.strip().split("\n"):
        try:
            token = _parse_token(line)
            tokens.append(token)
        except ValueError:
            pass
    tokens.append(Token("EOF", "", None, 2))
    return tokens


# prepare tokens
TOKENS = _text2tokens("""
                      NUMBER "2" 2.0
                      STAR * null
                      NUMBER "3.14" 3.14
                      """)
LAST = len(TOKENS) - 1


def test_Parser_assignment():
    assert Parser(_text2tokens("""IDENTIFIER pi null
                                  EQUAL = null
                                  NUMBER "3.14" 3.14""")).assignment() == Assign(Token("IDENTIFIER", "pi", None, 1), Literal(3.14))
    

def test_Parser_or():
    assert Parser(_text2tokens("""FALSE false null
                                  OR or null
                                  STRING "hello" hello""")).logic_or() == Logical(Literal(False), OR, Literal("hello"))


def test_Parser_and():
    assert Parser(_text2tokens("""TRUE true null
                                  AND and null
                                  STRING "hello" hello""")).logic_and() == Logical(Literal(True), AND, Literal("hello"))
    

def test_Parser_equality():
    assert Parser(_text2tokens("""STRING "yes" yes
                                  BANG_EQUAL != null
                                  STRING "ok" ok""")).equality() == Binary(Literal("yes"), NOT_EQUAL, Literal("ok"))


def test_Parser_comparison():
    assert Parser(_text2tokens("""NUMBER "12" 12.0
                                  LESS_EQUAL <= null
                                  NUMBER "33.3" 33.3""")).comparison() == Binary(Literal(12.0), LESS_EQUAL, Literal(33.3))
    

def test_Parser_term():
    assert Parser(_text2tokens("""NUMBER "12" 12.0
                                  PLUS + null
                                  NUMBER "2.5" 2.5""")).term() == Binary(Literal(12.0), PLUS, Literal(2.5))
    

def test_Parser_factor():
    assert Parser(_text2tokens("""NUMBER "12" 12.0
                                  SLASH / null
                                  NUMBER "2.5" 2.5""")).factor() == Binary(Literal(12.0), DIVISE, Literal(2.5))


def test_Parser_unary():
    assert Parser(_text2tokens("""MINUS - null
                                  NUMBER "12" 12.0""")).unary() == Unary(MINUS, Literal(12.0))
    assert Parser(_text2tokens("""STRING "test" test""")).unary() == Literal("test")


def test_Parser_call_no_arguments():
    tokens = _text2tokens("""IDENTIFIER "clock" clock
                             LEFT_PAREN ( null
                             RIGHT_PAREN ) null""")
    assert Parser(tokens).call() == Call(Variable(tokens[0]), tokens[2], arguments=tuple())


def test_Parser_call_two_arguments():
    tokens = _text2tokens("""IDENTIFIER "add" add
                             LEFT_PAREN ( null
                             NUMBER 1 1.0
                             COMMA , null
                             NUMBER 2 2.0
                             RIGHT_PAREN ) null""")
    assert Parser(tokens).call() == Call(Variable(tokens[0]), tokens[5], arguments=(Literal(1.0), Literal(2.0)))


def test_Parser_call_too_many_arguments(capsys):
    rawtokens = ['IDENTIFIER "add" add', 'LEFT_PAREN ( null']
    for _ in range(255):
        rawtokens.append("NUMBER 1 1.0")
        rawtokens.append("COMMA , null")
    rawtokens.append("NUMBER 5 5.0")
    rawtokens.append("RIGHT_PAREN ) null")
    tokens = _text2tokens("\n".join(rawtokens))

    c = Parser(tokens).call()

    assert isinstance(c, Call)
    assert c.callee == Variable(tokens[0])
    assert c.arguments[0] == Literal(1.0)
    assert capsys.readouterr()[1] == "[line 1] Error at '(': Can't have more than 255 arguments.\n"


def test_Parser_primary():
    p = Parser(TOKENS)
    assert p.primary() == Literal(2.0)
    assert Parser([Token("FALSE", "false", None, 1)]).primary() == Literal(False)
    assert Parser([Token("TRUE", "true", None, 1)]).primary() == Literal(True)
    assert Parser([Token("NIL", "nil", None, 1)]).primary() == Literal(None)
    assert Parser([Token("STRING", '"test"', "test", 1)]).primary() == Literal("test")

    grouping_tokens = _text2tokens("""LEFT_PAREN ( null
                                      NUMBER "3.14" 3.14
                                      RIGHT_PAREN ) null""")
    assert Parser(grouping_tokens).primary() == Grouping(Literal(3.14))

    assert Parser([Token("IDENTIFIER", "pi", None, 1)]).primary() == Variable(Token("IDENTIFIER", "pi", None, 1))
    
    assert Parser(_text2tokens("""SUPER super null
                                  DOT . null
                                  IDENTIFIER eat null
                                  LEFT_PAREN ( null
                                  RIGHT_PAREN ) null""")).primary() == Super(Token("SUPER", "super", None, 1),
                                                                             Token("IDENTIFIER", "eat", None, 1))


def test_Parser_primary_with_unterminated_parentheses():
    p = Parser(_text2tokens("""LEFT_PAREN ( null
                               STRING "fail" fail"""))
    with pytest.raises(ParserError) as ex:
        p.primary()
    assert ex.value.args[0] == (1, "Expected ')' after expression.", " at '('")


def test_Parser_peek():
    p = Parser(TOKENS)
    assert p.peek().toktype == "NUMBER"
    p.current = 1
    assert p.peek().toktype == "STAR"


def test_Parser_previous_token():
    p = Parser(TOKENS)
    p.advance()
    p.advance()
    p.advance()
    assert p.previous_token().toktype == "NUMBER"
    assert p.previous_token().literal == 3.14


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


def test_Parser_finish_call_no_arguments():
    tokens = _text2tokens("""IDENTIFIER "add" add
                             LEFT_PAREN ( null
                             RIGHT_PAREN ) null""")
    p = Parser(tokens)
    p.current = 2
    node = p.finish_call(Variable(tokens[0]))
    assert isinstance(node, Call)
    assert node.callee == Variable(tokens[0])
    assert node.paren == tokens[2]
    assert node.arguments == tuple()


def test_Parser_finish_call_with_unterminated_parentheses():
    tokens = _text2tokens("""IDENTIFIER "add" add
                             LEFT_PAREN ( null
                             NUMBER 2 2.0""")
    p = Parser(tokens)
    p.current = 2
    with pytest.raises(ParserError) as ex:
        p.finish_call(Variable(tokens[0]))
    assert ex.value.args[0] == (1, "Expected ')' after arguments.", " at '('")


def test_Parser_synchronize_post_error_with_semicolon():
    p = Parser(_text2tokens("""LEFT_PAREN ( null
                               STRING "fail" fail
                               SEMICOLON ; null
                               NUMBER 8 8.0"""))
    p.synchronize_post_error()
    assert p.match("NUMBER")


def test_Parser_synchronize_post_error_with_statement():
    p = Parser(_text2tokens("""LEFT_PAREN ( null
                               STRING "fail" fail
                               RETURN return null
                               NUMBER 8 8.0"""))
    p.synchronize_post_error()
    assert p.match("RETURN")


def test_Parser_synchronize_post_error_until_EOF():
    p = Parser(_text2tokens("""LEFT_PAREN ( null
                               STRING "fail" fail
                               NUMBER 8 8.0"""))
    p.synchronize_post_error()
    assert p.peek().toktype == "EOF"
