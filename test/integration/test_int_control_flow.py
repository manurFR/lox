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