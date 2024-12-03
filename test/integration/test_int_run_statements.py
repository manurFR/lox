from fixtures import run_lox


def test_evaluate_print(run_lox):
    _, output, _ = run_lox(command="run", lox_source='print "Hello World!";')
    assert output == "Hello World!"

    _, output, _ = run_lox(command="run", lox_source='print 42;')
    assert output == "42"

    _, output, _ = run_lox(command="run", lox_source='print true;')
    assert output == "true"

    _, output, _ = run_lox(command="run", lox_source='print 12 + 24;')
    assert output == "36"

    # _, output, _ = run_lox(command="run", lox_source='print "Missing semicolon->"')
    # assert output == "Hello World!"