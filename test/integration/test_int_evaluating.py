from fixtures import run_lox


def test_evaluate_literals(run_lox):
    _, output, _ = run_lox(command="evaluate", lox_source="true")
    assert output == "true"

    _, output, _ = run_lox(command="evaluate", lox_source="false")
    assert output == "false"

    _, output, _ = run_lox(command="evaluate", lox_source="nil")
    assert output == "nil"