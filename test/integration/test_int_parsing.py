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