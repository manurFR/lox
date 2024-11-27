from scanning import tokenize

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


def _format(tokens):
    return [repr(tok) for tok in tokens]