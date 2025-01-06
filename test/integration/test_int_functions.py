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

    # -- runtime errors --
    status, output, stderr = run_lox(command="run", lox_source="clock(25, 12, 2024);")
    assert status == 70
    assert output == ""
    assert stderr == "Expected 0 arguments but got 3.\n[line 1]"

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

    assert output == "5\n10\n<fn test>"

    # -- syntax errors --
    status, output, stderr = run_lox(command="run", lox_source="fun 3.14() {}")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at '3.14': Expected function name."

    status, output, stderr = run_lox(command="run", lox_source="fun no_leftparen {}")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'no_leftparen': Expected '(' after function name."

    status, output, stderr = run_lox(command="run", lox_source="fun no_param_name( {}")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'no_param_name': Expected parameter name."

    status, output, stderr = run_lox(command="run", lox_source="fun no_rightparen(a {}")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'no_rightparen': Expected ')' after parameters."

    status, output, stderr = run_lox(command="run", lox_source="fun no_braces() print 10;")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'no_braces': Expected '{' before function body."


def test_user_functions_with_arguments(run_lox):
    source = """
var a = 5;
fun add(a, b, c) { print a + b + c; }
print a;
add(24, 25, 26);
print add;
""".strip()
    
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "5\n75\n<fn add>"

    # -- syntax errors --
    status, output, stderr = run_lox(command="run", lox_source="fun no_comma(a, b c, d, e, f) {}\nno_comma();")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'no_comma': Expected ')' after parameters."

    # -- runtime error
    status, output, stderr = run_lox(command="run", lox_source="fun add(a, b) {print a+b;} \n add(1);")
    assert status == 70
    assert output == ""
    assert stderr == "Expected 2 arguments but got 1.\n[line 2]"


def test_user_functions_with_return(run_lox):
    source = """
fun fib(n) {
  if (n < 2) return n;
  return fib(n - 2) + fib(n - 1);
}

var start = clock();
print fib(20) == 6765;
print (clock() - start) < 5; // 5 seconds
"""

    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "true\ntrue"

    # no return statement
    _, output, _ = run_lox(command="run", lox_source="fun f() {var a=1;} print f();")
    assert output == "nil"
