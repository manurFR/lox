from fixtures import run_lox


def test_evaluate_literals(run_lox):
    _, output, _ = run_lox(command="evaluate", lox_source="true")
    assert output == "true"

    _, output, _ = run_lox(command="evaluate", lox_source="false")
    assert output == "false"

    _, output, _ = run_lox(command="evaluate", lox_source="nil")
    assert output == "nil"

    _, output, _ = run_lox(command="evaluate", lox_source='"hello world!"')
    assert output == "hello world!"

    _, output, _ = run_lox(command="evaluate", lox_source="10")
    assert output == "10"

    _, output, _ = run_lox(command="evaluate", lox_source="10.40")
    assert output == "10.4"
    
    _, output, _ = run_lox(command="evaluate", lox_source="12.000000")
    assert output == "12"


def test_evaluate_parentheses(run_lox):
    _, output, _ = run_lox(command="evaluate", lox_source="(true)")
    assert output == "true"

    _, output, _ = run_lox(command="evaluate", lox_source="( 10.40 )")
    assert output == "10.4"

    _, output, _ = run_lox(command="evaluate", lox_source="((false))")
    assert output == "false"


def test_evauate_unary_operators(run_lox):
    _, output, _ = run_lox(command="evaluate", lox_source="!true")
    assert output == "false"

    _, output, _ = run_lox(command="evaluate", lox_source="- (73)")
    assert output == "-73"

    _, output, _ = run_lox(command="evaluate", lox_source="!((nil))")
    assert output == "true"

    _, output, _ = run_lox(command="evaluate", lox_source='!"strings are truthy"')
    assert output == "false"
    