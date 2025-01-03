from fixtures import run_lox


def test_native_function_clock(run_lox):
    source = """
var c = clock() / 1000;
print c;
""".strip()
    
    status, output, _ = run_lox(command="run", lox_source=source)

    assert status == 0
    val = int(float(output.strip()))
    assert 1735900 < val < 1800000

    # -- syntax error --
    status, output, stderr = run_lox(command="run", lox_source="clock(25, 12, 2024);")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at '25': Expected ')' after arguments."

    # -- runtime error --
    status, output, stderr = run_lox(command="run", lox_source='"not_a_function"();')
    assert status == 70
    assert output == ""
    assert stderr == "Can only call functions and classes.\n[line 1]"


def test_user_functions_without_arguments(run_lox):
    source = """
var a = 5;
fun test() { var a = 10; print a; }
print a;
test();
print test;
""".strip()
    
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "5\n10\n<fun test>"

    # -- syntax errors --
    status, output, stderr = run_lox(command="run", lox_source="fun 3.14() {}")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at '3.14': Expected function name."

    status, output, stderr = run_lox(command="run", lox_source="fun no_leftparen {}")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'no_leftparen': Expected '(' after function name."

    status, output, stderr = run_lox(command="run", lox_source="fun no_rightparen( {}")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'no_rightparen': Expected ')' after parameters."

    status, output, stderr = run_lox(command="run", lox_source="fun no_braces() print 10;")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'no_braces': Expected '{' before function body."