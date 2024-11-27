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


def test_tokenize_equal(run_lox):
    status, output, _ = run_lox(command="tokenize", lox_source="={===}")

    assert status == 0

    assert output.split("\n") == """
EQUAL = null
LEFT_BRACE { null
EQUAL_EQUAL == null
EQUAL = null
RIGHT_BRACE } null
EOF  null
""".strip().split("\n")
    

def test_tokenize_not(run_lox):
    status, output, _ = run_lox(command="tokenize", lox_source="!!===")

    assert status == 0

    assert output.split("\n") == """
BANG ! null
BANG_EQUAL != null
EQUAL_EQUAL == null
EOF  null
""".strip().split("\n")
    

def test_tokenize_comparison_operators(run_lox):
    status, output, _ = run_lox(command="tokenize", lox_source="<<=>>=")

    assert status == 0

    assert output.split("\n") == """
LESS < null
LESS_EQUAL <= null
GREATER > null
GREATER_EQUAL >= null
EOF  null
""".strip().split("\n")


def test_tokenize_comments(run_lox):
    status, output, _ = run_lox(command="tokenize", lox_source="/()// Comment")

    assert status == 0

    assert output.split("\n") == """
SLASH / null
LEFT_PAREN ( null
RIGHT_PAREN ) null
EOF  null
""".strip().split("\n")


def test_whitespaces_newlines(run_lox):
    status, output, stderr = run_lox(command="tokenize", lox_source="""
# (\t 
 )
         $""".strip())  # invalid characters on lines 1 and 3

    assert output.split("\n") == """
LEFT_PAREN ( null
RIGHT_PAREN ) null
EOF  null
""".strip().split("\n")
    
    assert stderr.split("\n") == """
[line 1] Error: Unexpected character: #
[line 3] Error: Unexpected character: $
""".strip().split("\n")
    
    assert status == 65
