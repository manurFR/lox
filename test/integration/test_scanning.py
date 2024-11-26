from fixtures import run_lox


def test_tokenize_parentheses(run_lox):
    output = run_lox(command="tokenize", lox_source="(()")

    assert output.split("\n") == [
        "LEFT_PAREN ( null",
        "LEFT_PAREN ( null",
        "RIGHT_PAREN ) null",
        "EOF  null"
    ]


def test_tokenize_braces(run_lox):
    output = run_lox(command="tokenize", lox_source="{{}}")

    assert output.split("\n") == [
        "LEFT_BRACE { null",
        "LEFT_BRACE { null",
        "RIGHT_BRACE } null",
        "RIGHT_BRACE } null",
        "EOF  null"
    ]