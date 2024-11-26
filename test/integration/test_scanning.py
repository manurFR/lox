from fixtures import run_lox


def test_tokenize_parentheses(run_lox):
    _, output, _ = run_lox(command="tokenize", lox_source="(()")

    assert output.split("\n") == [
        "LEFT_PAREN ( null",
        "LEFT_PAREN ( null",
        "RIGHT_PAREN ) null",
        "EOF  null"
    ]


def test_tokenize_braces(run_lox):
    _, output, _ = run_lox(command="tokenize", lox_source="{{}}")

    assert output.split("\n") == [
        "LEFT_BRACE { null",
        "LEFT_BRACE { null",
        "RIGHT_BRACE } null",
        "RIGHT_BRACE } null",
        "EOF  null"
    ]


def test_tokenize_all_single_characters(run_lox):
    status, output, _ = run_lox(command="tokenize", lox_source="(-{*.,+*};)")

    assert status == 0

    assert output.split("\n") == """
LEFT_PAREN ( null
MINUS - null
LEFT_BRACE { null
STAR * null
DOT . null
COMMA , null
PLUS + null
STAR * null
RIGHT_BRACE } null
SEMICOLON ; null
RIGHT_PAREN ) null
EOF  null
""".strip().split("\n")
    

def test_tokenize_lexical_errors(run_lox):
    status, output, stderr = run_lox(command="tokenize", lox_source=",.$(#")

    assert output.split("\n") == """
COMMA , null
DOT . null
LEFT_PAREN ( null
EOF  null
""".strip().split("\n")
    
    assert stderr.split("\n") == """
[line 1] Error: Unexpected character: $
[line 1] Error: Unexpected character: #
""".strip().split("\n")
    
    assert status == 65