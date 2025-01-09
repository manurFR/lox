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
    
    _, output, stderr = run_lox(command="run", lox_source=source)

    assert stderr == ""
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


def test_class_instanciation(run_lox):
    source = """
class Bagel {}
var bagel = Bagel();
print bagel;
""".strip()
    
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "<instanceof Bagel>"


def test_instance_properties(run_lox):
    source = """
class Breakfast {}
var breakfast = Breakfast();
class Tea {}
var tea = Tea();
breakfast.hotdrink = tea;  // setting
breakfast.hotdrink.sugars = 1;  // setting at the end of a chain
print tea.sugars;  // getting
""".strip()
    
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "1"

    # -- syntax errors --
    status, output, stderr = run_lox(command="run", lox_source="class Test {} var t = Test(); t. = 3;")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at '.': Expected property name after '.'."

    # -- runtime errors --
    status, output, stderr = run_lox(command="run", lox_source='var a = "not instance"; print a.property;')
    assert status == 70
    assert output == ""
    assert stderr == "Only class instances have properties callable by '.'.\n[line 1]"

    status, output, stderr = run_lox(command="run", lox_source='class Test {} var t = Test(); print t.missing;')
    assert status == 70
    assert output == ""
    assert stderr == "Undefined property 'missing'.\n[line 1]"

    status, output, stderr = run_lox(command="run", lox_source='var a = "not instance"; a.property = 1;')
    assert status == 70
    assert output == ""
    assert stderr == "Only class instances have fields.\n[line 1]"


def test_calling_instance_methods(run_lox):
    source = """
class Bacon {
    eat() { print "Yummy!"; }
}
Bacon().eat();
""".strip()
    
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "Yummy!"


def test_methods_using_this(run_lox):
    source = """
class Cake {
  taste() {
    var adjective = "delicious";
    print "This " + this.flavor + " cake is " + adjective + "!";
  }
}

var cake = Cake();
cake.flavor = "chocolate";
cake.taste();

var cake2 = Cake();
cake2.flavor = "cinnamon";
cake.taste = cake2.taste;  // the copied taste() function should keep 'this' referencing the cake2 flavor
cake.taste();
""".strip()
    
    _, output, _ = run_lox(command="run", lox_source=source)

    assert output == "This chocolate cake is delicious!\nThis cinnamon cake is delicious!"

    # -- syntax errors --
    status, output, stderr = run_lox(command="run", lox_source="fun notAMethod() {print this;}")
    assert status == 65
    assert output == ""
    assert stderr == "[line 1] Error at 'this': Can't use 'this' outside of a class."