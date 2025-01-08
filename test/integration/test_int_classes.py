from fixtures import run_lox


def test_class_declaration(run_lox):
    source = """
class MapleSyrup {
  serveOn() {
    return "Pancakes";
  }
}

print MapleSyrup;
""".strip()
    
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "<class MapleSyrup>"

    # -- syntax errors --
    status, output, stderr = run_lox(command="run", lox_source="class {}")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at '{': Expected class name."

    status, output, stderr = run_lox(command="run", lox_source="class no_leftbrace")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'no_leftbrace': Expected '{' before class body."

    status, output, stderr = run_lox(command="run", lox_source="class no_methods {1;}")
    assert status == 65
    assert output == ""
    assert stderr.startswith("[line 1] Error at '1': Expected method name.")

    status, output, stderr = run_lox(command="run", lox_source="class no_rightbrace { method1() {print 1;}")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'no_rightbrace': Expected '}' after class body."
    