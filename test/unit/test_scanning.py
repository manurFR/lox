import string
from scanning import tokenize, lookahead_capture  # type: ignore

"""
$ PYTHONPATH=app pytest -vv -k unit
"""


def test_tokenize_empty():
    tokens, errors = tokenize("")

    assert errors == []
    
    assert _format(tokens) == ["EOF  null"]


def test_tokenize_single_characters():
    tokens, errors = tokenize("(*.$}")

    assert errors == [(1, "Unexpected character: $")]

    assert _format(tokens) == """
LEFT_PAREN ( null
STAR * null
DOT . null
RIGHT_BRACE } null
EOF  null
""".strip().split("\n")


def test_tokenize_two_characters():
    tokens, _ = tokenize("=!./==!==><=>=<")

    assert _format(tokens) == """
EQUAL = null
BANG ! null
DOT . null
SLASH / null
EQUAL_EQUAL == null
BANG_EQUAL != null
EQUAL = null
GREATER > null
LESS_EQUAL <= null
GREATER_EQUAL >= null
LESS < null
EOF  null
""".strip().split("\n")
    

def test_tokenize_comments():
    tokens, _ = tokenize("()// Comment")

    assert _format(tokens) == """
LEFT_PAREN ( null
RIGHT_PAREN ) null
EOF  null
""".strip().split("\n")


def test_tokenize_whitespaces_newlines():
    tokens, errors = tokenize("( \t )\n   *  .")

    assert len(errors) == 0

    assert _format(tokens) == """
LEFT_PAREN ( null
RIGHT_PAREN ) null
STAR * null
DOT . null
EOF  null
""".strip().split("\n")
    

def test_tokenize_comments_should_increment_line_count():
    tokens, errors = tokenize("""
()  #\t{}
@
+++
-// Let's Go!
#
""".strip())

    assert errors == [(1, "Unexpected character: #"),
                      (2, "Unexpected character: @"),
                      (5, "Unexpected character: #")]

    assert _format(tokens) == """
LEFT_PAREN ( null
RIGHT_PAREN ) null
LEFT_BRACE { null
RIGHT_BRACE } null
PLUS + null
PLUS + null
PLUS + null
MINUS - null
EOF  null
""".strip().split("\n")
    

def test_tokenize_string_literals():
    tokens, _ = tokenize('("foo baz"')

    assert _format(tokens) == """
LEFT_PAREN ( null
STRING "foo baz" foo baz
EOF  null
""".strip().split("\n")


def test_tokenize_unterminated_string():
    tokens, errors = tokenize('''
                              *
                                 "no end to this string
                              ()'''.strip())

    assert errors == [(2, "Unterminated string.")]

    assert _format(tokens) == """
STAR * null
EOF  null
""".strip().split("\n")
    

def test_tokenize_numbers():
    tokens, _ = tokenize("/12.34/")

    assert _format(tokens) == """
SLASH / null
NUMBER 12.34 12.34
SLASH / null
EOF  null
""".strip().split("\n")
    

def test_tokenize_integers():
    tokens, _ = tokenize("12")

    assert _format(tokens) == """
NUMBER 12 12.0
EOF  null
""".strip().split("\n")


def test_tokenize_identifiers():
    tokens, _ = tokenize('* hello ; "hello" ; big_word ; _underscore123_ ')

    assert _format(tokens) == """
STAR * null
IDENTIFIER hello null
SEMICOLON ; null
STRING "hello" hello
SEMICOLON ; null
IDENTIFIER big_word null
SEMICOLON ; null
IDENTIFIER _underscore123_ null
EOF  null
""".strip().split("\n")
    

def test_tokenize_reserved_words():
    tokens, _ = tokenize('orchid or function for fun')

    assert _format(tokens) == """
IDENTIFIER orchid null
OR or null
IDENTIFIER function null
FOR for null
FUN fun null
EOF  null
""".strip().split("\n")


def test_lookahead_capture():
    assert lookahead_capture(remaining="456>>>", valid_chars=string.digits) == ("456", 2)
    assert lookahead_capture(remaining="456", valid_chars=string.digits) == ("456", 2)
    assert lookahead_capture(remaining="4.56<<<", valid_chars=string.digits, valid_sep='.') == ("4.56", 3)
    assert lookahead_capture(remaining="4.56", valid_chars=string.digits, valid_sep='.') == ("4.56", 3)
    assert lookahead_capture(remaining="45.#", valid_chars=string.digits, valid_sep='.') == ("45", 1)
    assert lookahead_capture(remaining="45.", valid_chars=string.digits, valid_sep='.') == ("45", 1)


def _format(tokens):
    return [repr(tok) for tok in tokens]