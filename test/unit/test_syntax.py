from scanning import Token  # type: ignore
from syntax import Assign, Binary, Block, Expression, Grouping, Literal, Print, Unary, Var, Variable # type: ignore
from tokens import MINUS, MULTIPLY, NOT


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

def test_Variable_repr():
    assert repr(Variable(Token("IDENTIFIER", "count", None, 1))) == "count"


def test_Assign_repr():
    assert repr(Assign(Token("IDENTIFIER", "count", None, 1), Literal(5))) == "count = 5"


# Statement classes
def test_Expression_repr():
    assert repr(Expression(Unary(MINUS, Literal(5.5)))) == "(- 5.5)"


def test_Print_repr():
    assert repr(Print(Literal("hello"))) == 'print hello;'


def test_Var_repr():
    assert repr(Var(Token("IDENTIFIER", "pi", None, 1), Literal(3.14))) == "var pi = 3.14;"
    assert repr(Var(Token("IDENTIFIER", "area", None, 1), None)) == "var area;"


def test_Block_repr():
    assert repr(Block([])) == "{}"
    assert repr(Block([Var(Token("IDENTIFIER", "word", None, 1), Literal("test")), 
                       Print(Variable(Token("IDENTIFIER", "word", None, 1)))])) == "{var word = test;\nprint word;}"