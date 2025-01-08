from fixtures import run_lox


def test_regular_closure(run_lox):
    source = """
fun makeCounter() {
  var i = 0;
  fun count() {
    i = i + 1;  // closure! i is declared in the body of the enclosing element
    return i;
  }

  return count;
}

var counter = makeCounter();
print counter(); // "1".
print counter(); // "2".
""".strip()

    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "1\n2"


def test_static_scope(run_lox):
    source = """
var a = "global";
{
  fun showA() {
    print a;  // should ALWAYS print "global" because the scope of showA() show be invariant, ie. the one at the time the function is defined
  }

  showA();
  var a = "block";
  showA();
}
""".strip()

    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "global\nglobal"
