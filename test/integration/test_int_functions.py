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