from fixtures import run_lox


def test_parse_literals(run_lox):
    _, output, _ = run_lox(command="parse", lox_source="true")
    assert output == "true"

    _, output, _ = run_lox(command="parse", lox_source="nil")
    assert output == "nil"

    _, output, _ = run_lox(command="parse", lox_source="12.34")
    assert output == "12.34"
