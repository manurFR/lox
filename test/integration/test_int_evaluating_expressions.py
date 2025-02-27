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
    

def test_evaluate_binary_operators(run_lox):
    _, output, _ = run_lox(command="evaluate", lox_source="3 * 5")
    assert output == "15"

    _, output, _ = run_lox(command="evaluate", lox_source="42/5")
    assert output == "8.4"

    _, output, _ = run_lox(command="evaluate", lox_source="18 * 3 / (3 * 6)")
    assert output == "3"

    _, output, _ = run_lox(command="evaluate", lox_source="(10.40 * 2) / 2")
    assert output == "10.4"

    _, output, _ = run_lox(command="evaluate", lox_source="69 - 93")
    assert output == "-24"

    _, output, _ = run_lox(command="evaluate", lox_source="23 + 28 - (-(61 - 99)  )")
    assert output == "13"

    _, output, _ = run_lox(command="evaluate", lox_source='"hello" + " world!"')
    assert output == "hello world!"

    _, output, _ = run_lox(command="evaluate", lox_source='"42"+"24"')
    assert output == "4224"

    _, output, _ = run_lox(command="evaluate", lox_source="10>5")
    assert output == "true"

    _, output, _ = run_lox(command="evaluate", lox_source="11 <= 11.0")
    assert output == "true"

    _, output, _ = run_lox(command="evaluate", lox_source="(54 - 67) < -(114 / 57 + 11)")
    assert output == "false"

    _, output, _ = run_lox(command="evaluate", lox_source="12 == 12.0")
    assert output == "true"

    _, output, _ = run_lox(command="evaluate", lox_source='"foo" == "bar"')
    assert output == "false"

    _, output, _ = run_lox(command="evaluate", lox_source='61 == "61"')
    assert output == "false"

    _, output, _ = run_lox(command="evaluate", lox_source='"foo" != "bar"')
    assert output == "true"


def test_runtime_errors(run_lox):
    status, _, stderr = run_lox(command="evaluate", lox_source='-"hellow world!"')
    assert status == 70
    assert stderr.split("\n") == """
Operand must be a number.
[line 1]
""".strip().split("\n")
    
    status, _, stderr = run_lox(command="evaluate", lox_source='"foo" * 42')
    assert status == 70
    assert stderr.split("\n") == """
Operands must be numbers.
[line 1]
""".strip().split("\n")
    
    status, _, stderr = run_lox(command="evaluate", lox_source="false / true")
    assert status == 70
    assert stderr.split("\n") == """
Operands must be numbers.
[line 1]
""".strip().split("\n")
    
    status, _, stderr = run_lox(command="evaluate", lox_source='666 - "hell"')
    assert status == 70
    assert stderr.split("\n") == """
Operands must be numbers.
[line 1]
""".strip().split("\n")
    
    status, _, stderr = run_lox(command="evaluate", lox_source="true + false")
    assert status == 70
    assert stderr.split("\n") == """
Operands must be two numbers or two strings.
[line 1]
""".strip().split("\n")
    
    status, _, stderr = run_lox(command="evaluate", lox_source="false >= 50")
    assert status == 70
    assert stderr.split("\n") == """
Operands must be numbers.
[line 1]
""".strip().split("\n")
    
    status, _, stderr = run_lox(command="evaluate", lox_source='("foo" + "bar") < 42')
    assert status == 70
    assert stderr.split("\n") == """
Operands must be numbers.
[line 1]
""".strip().split("\n")