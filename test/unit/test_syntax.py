from syntax import Binary, Grouping, Literal, Unary # type: ignore
from tokens import MINUS, MULTIPLY, NOT


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