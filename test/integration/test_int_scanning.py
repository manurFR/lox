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


def test_tokenize_whitespaces_newlines(run_lox):
    status, output, stderr = run_lox(command="tokenize", lox_source="""
# (\t 
 )  // cool remark
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


def test_tokenize_multiline_strings(run_lox):
    status, output, stderr = run_lox(command="tokenize", lox_source='''
/"hello"
+  "this is
a multi-line
string"
$'''.strip())  # invalid caracters on line 5, including newlines inside the string

    assert output.split("\n") == """
SLASH / null
STRING "hello" hello
PLUS + null
STRING "this is\na multi-line\nstring" this is\na multi-line\nstring
EOF  null
""".strip().split("\n")
    
    assert stderr.split("\n") == """
[line 5] Error: Unexpected character: $
""".strip().split("\n")
    
    assert status == 65


def test_tokenize_identifiers(run_lox):
    status, output, _ = run_lox(command="tokenize", lox_source="foo bar _hello")

    assert status == 0

    assert output.split("\n") == """
IDENTIFIER foo null
IDENTIFIER bar null
IDENTIFIER _hello null
EOF  null
""".strip().split("\n")
    

def test_tokenize_reserved_words(run_lox):
    status, output, _ = run_lox(command="tokenize", lox_source="""
var r = 3.14
if (r * r) >= 4 {
    print "found!"
} else return;""".strip())

    assert status == 0

    assert output.split("\n") == """
VAR var null
IDENTIFIER r null
EQUAL = null
NUMBER 3.14 3.14
IF if null
LEFT_PAREN ( null
IDENTIFIER r null
STAR * null
IDENTIFIER r null
RIGHT_PAREN ) null
GREATER_EQUAL >= null
NUMBER 4 4.0
LEFT_BRACE { null
PRINT print null
STRING "found!" found!
RIGHT_BRACE } null
ELSE else null
RETURN return null
SEMICOLON ; null
EOF  null
""".strip().split("\n")
