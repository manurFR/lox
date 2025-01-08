from fixtures import run_lox


def test_if_statement(run_lox):
    source = """
var stage = "unknown";
var age = 50;
if (age < 18) { stage = "child"; }
if (age >= 18) { stage = "adult"; }
print stage;

var isAdult = age >= 18;
if (isAdult) { print "eligible for voting: true"; }
if (!isAdult) { print "eligible for voting: false"; }
""".strip()
    _, output, _ = run_lox(command="run", lox_source=source)
    assert output == "adult\neligible for voting: true"

    # tricky play with '=' and '=='
    _, output, _ = run_lox(command="run", lox_source="var a = false; if (a = true) {print(a == true);}")
    assert output == "true"

    # else
    source = """
var a = 5;
if (a < 3) print "less than 3";
else print "more than 3";
""".strip()
    _, output, _ = run_lox(command="run", lox_source=source)
    assert output == "more than 3"

    # else if
    source = """
var age = 88;
var stage = "unknown";
if (age < 18) { stage = "child"; }
else if (age < 65) { stage = "adult"; }
else if (age < 100) { stage = "senior"; }
else if (age >= 100) { stage = "centenarian"; }
print stage;
""".strip()
    _, output, _ = run_lox(command="run", lox_source=source)
    assert output == "senior"

    # nested ifs
    _, output, _ = run_lox(command="run", lox_source='if (true) if (false) print "world"; else print "baz";')
    assert output == "baz"


def test_logical_operators(run_lox):
    source = """
print 41 or true;
print false or 41;
print false or false or true;
print false or false;
var a = "hello";
var b = "hello";
(a = false) or (b = true) or (a = "hello");
print a;
print b;
""".strip()
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "41\n41\ntrue\nfalse\nfalse\ntrue"

    source = """
print false and 41;
if (true and "hello") print "yes";
print true or true and false;
""".strip()
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "false\nyes\ntrue"


def test_while_statement(run_lox):
    source = """
while (false) {
  print "should not print";
}
var product = 1;
var i = 1;
while (i <= 5) {
  product = product * i;
  i = i + 1;
}
print product;
var foo = 0;
while (foo < 3) print foo = foo + 1;
""".strip()
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "120\n1\n2\n3"


def test_for_statement(run_lox):
    source = """
var baz = "hello";
for (var baz = 0; baz < 3; baz = baz + 1) {
    print baz;
}
print baz;
""".strip()
    
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "0\n1\n2\nhello"

    # -- syntax error --
    status, output, stderr = run_lox(command="run", lox_source="for ({}; a < 2; a = a + 1) {}")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at '{': Expected expression."


def test_break_statement(run_lox):
    source = """
var a = 1;
while (a < 10) {
    print a;
    if (a == 2) break;
    a = a + 1;
}
""".strip()
    
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "1\n2"

    source = """
var test = 1;
while (test < 3) {
    for (var i = 0; i < 5; i = i + 1) {
        print i;
        if (i == 2) {
            test = test + 1;
            break;
        }
    }
}
""".strip()
    
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "0\n1\n2\n0\n1\n2"


def test_continue_statement(run_lox):
    source = """
for (var i = 0; i < 5; i = i + 1) {
    if (i == 2 or i == 3) continue;
    print i;
}
""".strip()
    
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "0\n1\n4"


def test_error_return_at_top_level(run_lox):
    status, output, stderr = run_lox(command="run", lox_source='return "at top level!";')

    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'return': Can't use 'return' in top-level code."


def test_error_break_or_continue_at_top_level(run_lox):
    status, output, stderr = run_lox(command="run", lox_source='break;')

    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'break': Can't use 'break' outside of loop."

    status, output, stderr = run_lox(command="run", lox_source='if (true) { continue; }')

    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'continue': Can't use 'continue' outside of loop."