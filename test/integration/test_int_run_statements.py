from fixtures import run_lox


def test_run_print(run_lox):
    _, output, _ = run_lox(command="run", lox_source='print "Hello World!";')
    assert output == "Hello World!"

    _, output, _ = run_lox(command="run", lox_source='print 42;')
    assert output == "42"

    _, output, _ = run_lox(command="run", lox_source='print true;')
    assert output == "true"

    _, output, _ = run_lox(command="run", lox_source='print 12 + 24;')
    assert output == "36"

    # multi-lines
    source = """
print "world" + "baz" + "bar";
print 27 - 26;
print "bar" == "quz";
""".strip()
    status, output, _ = run_lox(command="run", lox_source=source)
    
    assert status == 0
    
    assert output == """
worldbazbar
1
false""".strip()

    # -- syntax error --
    status, output, stderr = run_lox(command="run", lox_source='print "Missing semicolon->"')
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'print': Expected ';' after value."


def test_run_expression_statements(run_lox):
    # expression statement results are discarded... the side-effects are their interesting parts.
    source = """
(37 + 42 - 21) > (76 - 37) * 2;
print !false;
"baz" + "hello" + "quz" + "bar" == "bazhelloquzbar";
print !false;
""".strip()
    _, output, _ = run_lox(command="run", lox_source=source)
    
    assert output == "true\ntrue"

    # -- runtime error --
    source = """
print "the expression below is invalid";
49 + "baz";
print "this should not be printed";""".strip()
    status, output, stderr = run_lox(command="run", lox_source=source)
    
    assert status == 70

    assert output == "the expression below is invalid"
    assert stderr == "Operands must be two numbers or two strings.\n[line 2]"

    # -- syntax error --
    status, output, stderr = run_lox(command="run", lox_source='"Missing" + "semicolon->"')
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at '\"Missing\"': Expected ';' after expression."


def test_run_variable_declaration_and_accessing(run_lox):
    source = """
var a = "foo";
print a ;
var bar = 99;
var foo = 99;
print bar + foo;
var quz = 99;
print bar + foo + quz;
var a = quz;
var b = 2;
print (8*(a + b)) / 202 + (100 - bar); // 8*101/202 + 1
""".strip()
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "foo\n198\n297\n5"

    source = """
var baz = "foo";
var bar;
print bar;""".strip()
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "nil"

    # -- runtime error --
    source = """
print 22;
var hello = 85;
var world = 12;
var result = (hello + bar) / world;
""".strip()
    status, output, stderr = run_lox(command="run", lox_source=source)

    assert output == "22"

    assert status == 70
    assert stderr == "Undefined variable 'bar'.\n[line 4]"


def test_run_variable_assignment(run_lox):
    source = """
var quz;
var hello;

quz = hello = 16 + 34 * 92;
print quz;
print hello;
""".strip()
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "3144\n3144"


def test_run_block_declarations(run_lox):
    source = """
{
    var foo = "before";
    print foo;
}
{
    var foo = "after";
    print foo;
}
""".strip()
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "before\nafter"

    # -- syntax error --
    status, output, stderr = run_lox(command="run", lox_source="{print 12.345;")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at '{': Expected '}' after block."