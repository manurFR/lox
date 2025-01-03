from scanning import Token  # type: ignore
from syntax import Assign, Binary, Block, Call, Expression, Grouping, If, Literal, Logical, Print, Unary, Var, Variable, While # type: ignore
from tokens import AND, GREATER, LESS, MINUS, MULTIPLY, NOT, OR, PLUS


# Expression classes
def test_Binary_repr():
    assert repr(Binary(Literal(2.5), MULTIPLY, Literal(4.0))) == "(* 2.5 4.0)"


def test_Unary_repr():
    assert repr(Unary(MINUS, Literal(5.5))) == "(- 5.5)"
    assert repr(Unary(NOT, Literal(False))) == "(! false)"


def test_Grouping_repr():
    assert repr(Grouping(Literal(5.5))) == "(group 5.5)"
    assert repr(Grouping(Literal(False))) == "(group false)"


def test_Literal_repr():
    assert repr(Literal(True)) == "true"
    assert repr(Literal(False)) == "false"
    assert repr(Literal(None)) == "nil"
    assert repr(Literal("test")) == "test"
    assert repr(Literal(12.34)) == "12.34"


def test_Logical_repr():
    assert repr(Logical(Literal(False), OR, Literal("hello"))) == "false or hello"
    assert repr(Logical(Binary(Literal(6.3), GREATER, Literal(2.9)), AND, Literal(True))) == "(> 6.3 2.9) and true"


def test_Variable_repr():
    assert repr(Variable(Token("IDENTIFIER", "count", None, 1))) == "count"


def test_Assign_repr():
    assert repr(Assign(Token("IDENTIFIER", "count", None, 1), Literal(5))) == "count = 5"


def test_Call_repr():
    assert repr(Call(Literal("add"), Token("LEFT_PAREN", "(", None, 1), [Literal(2), Literal(3)])) == "add(2, 3)"


# Statement classes
def test_Expression_repr():
    assert repr(Expression(Unary(MINUS, Literal(5.5)))) == "(- 5.5)"


def test_If_repr():
    assert repr(If(Binary(Literal(9.0), GREATER, Binary(Literal(3.5), MULTIPLY, Literal(2.5))), Print(Literal("Greater")), None)) == \
        "if ((> 9.0 (* 3.5 2.5))) then print greater;"
    assert repr(If(Literal(False), Print(Literal("it's wrong")), Print(Literal("it's true")))) == \
        "if (false) then print it's wrong; else print it's true;"


def test_Print_repr():
    assert repr(Print(Literal("hello"))) == 'print hello;'


def test_Var_repr():
    assert repr(Var(Token("IDENTIFIER", "pi", None, 1), Literal(3.14))) == "var pi = 3.14;"
    assert repr(Var(Token("IDENTIFIER", "area", None, 1), None)) == "var area;"


def test_While_repr():
    a = Token("IDENTIFIER", "a", None, 1)
    assert repr(While(Binary(Variable(a), LESS, Literal(10.0)), 
                      Print(Assign(a, Binary(Variable(a), PLUS, Literal(1.0)))), 
                      increment=None)) == "while ((< a 10.0)) print a = (+ a 1.0);"


def test_Block_repr():
    assert repr(Block([])) == "{}"
    assert repr(Block([Var(Token("IDENTIFIER", "word", None, 1), Literal("test")), 
                       Print(Variable(Token("IDENTIFIER", "word", None, 1)))])) == "{var word = test;\nprint word;}"