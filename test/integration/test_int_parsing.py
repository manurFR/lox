from fixtures import run_lox


def test_parse_literals(run_lox):
    _, output, _ = run_lox(command="parse", lox_source="true")
    assert output == "true"

    _, output, _ = run_lox(command="parse", lox_source="nil")
    assert output == "nil"

    _, output, _ = run_lox(command="parse", lox_source="12.34")
    assert output == "12.34"

    _, output, _ = run_lox(command="parse", lox_source='"hello"')
    assert output == "hello"

    _, output, _ = run_lox(command="parse", lox_source='("foo")')
    assert output == "(group foo)"


def test_parse_unary_operators(run_lox):
    _, output, _ = run_lox(command="parse", lox_source='!true')
    assert output == "(! true)"

    _, output, _ = run_lox(command="parse", lox_source='!!true')
    assert output == "(! (! true))"


def test_parse_arithmetic_operators(run_lox):
    _, output, _ = run_lox(command="parse", lox_source='16 * -38 / 58')
    assert output == "(/ (* 16.0 (- 38.0)) 58.0)"

    _, output, _ = run_lox(command="parse", lox_source='-52 + 80 + 7.7 - 94')
    assert output == "(- (+ (+ (- 52.0) 80.0) 7.7) 94.0)"


def test_parse_comparison_operators(run_lox):
    _, output, _ = run_lox(command="parse", lox_source="83 < 99 <= 115")
    assert output == "(<= (< 83.0 99.0) 115.0)"


def test_parse_equality_operators(run_lox):
    _, output, _ = run_lox(command="parse", lox_source='"baz" == "baz"')
    assert output == "(== baz baz)"


def test_parse_unterminated_parentheses(run_lox):
    status, output, stderr = run_lox(command="parse", lox_source="(12")
    assert output == 'None'

    assert status == 65

    assert stderr.split("\n") == """
[line 1] Error at '(': Expected ')' after expression.
""".strip().split("\n")


def test_parse_empty(run_lox):
    status, output, stderr = run_lox(command="parse", lox_source="")
    assert output == 'None'

    assert status == 65

    assert stderr.split("\n") == """
[line 1] Error at end: Expected expression.
""".strip().split("\n")