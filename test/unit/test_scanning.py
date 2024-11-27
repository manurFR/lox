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
    tokens, _ = tokenize("=!.==!==><=>=<")

    assert _format(tokens) == """
EQUAL = null
BANG ! null
DOT . null
EQUAL_EQUAL == null
BANG_EQUAL != null
EQUAL = null
GREATER > null
LESS_EQUAL <= null
GREATER_EQUAL >= null
LESS < null
EOF  null
""".strip().split("\n")


def _format(tokens):
    return [repr(tok) for tok in tokens]