import pytest
from evaluating import Interpreter, LoxRuntimeError  # type: ignore
from syntax import Literal, Grouping, Unary, Binary  # type: ignore
from tokens import DIVISE, EQUAL_EQUAL, GREATER, GREATER_EQUAL, LESS, LESS_EQUAL, MINUS, MULTIPLY, NOT, NOT_EQUAL, PLUS

@pytest.fixture
def interpreter():
    return Interpreter()


def test_evaluate_literal_number(interpreter):
    assert interpreter.evaluate(Literal(12.345)) == 12.345
    assert interpreter.evaluate(Literal(12.3450)) == 12.345
    assert interpreter.evaluate(Literal(12.34506)) == 12.34506
    assert interpreter.evaluate(Literal(12.0)) == 12
    assert interpreter.evaluate(Literal(12)) == 12


def test_evaluate_literal_others(interpreter):
    assert interpreter.evaluate(Literal(True)) == True
    assert interpreter.evaluate(Literal(False)) == False
    assert interpreter.evaluate(Literal(None)) == None
    assert interpreter.evaluate(Literal("python")) == "python"


def test_evaluate_grouping(interpreter):
    assert interpreter.evaluate(Grouping(Literal(None))) == None
    assert interpreter.evaluate(Grouping(Literal(25.60))) == 25.6
    assert interpreter.evaluate(Grouping(Grouping(Literal("so much parentheses!")))) == "so much parentheses!"


def test_evaluate_unary(interpreter):
    assert interpreter.evaluate(Unary(NOT, Literal(False))) == True
    assert interpreter.evaluate(Unary(NOT, Literal(None))) == True
    assert interpreter.evaluate(Unary(NOT, Literal(True))) == False
    assert interpreter.evaluate(Unary(NOT, Literal(3.14))) == False
    assert interpreter.evaluate(Unary(NOT, Literal("string"))) == False
    
    assert interpreter.evaluate(Unary(MINUS, Literal(3.14))) == -3.14
    assert interpreter.evaluate(Unary(MINUS, Grouping(Literal(12.0)))) == -12


def test_evaluate_arithmetic_operators(interpreter):
    assert interpreter.evaluate(Binary(Literal(10), MULTIPLY, Literal(2.5))) == 25
    assert interpreter.evaluate(Binary(Literal(10), DIVISE, Literal(4))) == 2.5
    # 6 * 2.5 / (2 * 3) => (/ (* 6.0 2.5) (group (* 2.0 3.0)))
    assert interpreter.evaluate(
        Binary(Binary(Literal(6), MULTIPLY, Literal(2.5)), DIVISE, Grouping(Binary(Literal(2), MULTIPLY, Literal(3))))) == 2.5

    assert interpreter.evaluate(Binary(Literal(12.8), MINUS, Literal(4.3))) == 8.5
    assert interpreter.evaluate(Binary(Literal(12.8), PLUS, Literal(4.3))) == 17.1
    # 6 + 4 * 3 == 18 => (+ 6.0 (* 4.0 3.0))
    assert interpreter.evaluate(Binary(Literal(6), PLUS, Binary(Literal(4), MULTIPLY, Literal(3)))) == 18
    # (6 + 4) * 3 == 30 => (* (group (+ 6.0 4.0)) 3.0)
    assert interpreter.evaluate(Binary(Grouping(Binary(Literal(6), PLUS, Literal(4))), MULTIPLY, Literal(3))) == 30


def test_evaluate_string_concatenation(interpreter):
    assert interpreter.evaluate(Binary(Literal("post"), PLUS, Literal("rock"))) == "postrock"


def test_comparison_operators(interpreter):
    assert interpreter.evaluate(Binary(Literal(12.3), GREATER, Literal(3.14))) is True
    assert interpreter.evaluate(Binary(Literal(12.3), LESS_EQUAL, Literal(3.14))) is False
    assert interpreter.evaluate(Binary(Literal(12.3), LESS_EQUAL, Literal(12.30))) is True
    assert interpreter.evaluate(Binary(Literal(12.3), GREATER_EQUAL, Literal(12.30))) is True
    assert interpreter.evaluate(Binary(Literal(12.3), GREATER_EQUAL, Literal(0))) is True
    assert interpreter.evaluate(Binary(Literal(-8), LESS, Literal(0))) is True


def test_equality_operators(interpreter):
    assert interpreter.evaluate(Binary(Literal(12.0), EQUAL_EQUAL, Literal(12))) is True
    assert interpreter.evaluate(Binary(Literal("test"), EQUAL_EQUAL, Literal("test"))) is True
    assert interpreter.evaluate(Binary(Literal(True), EQUAL_EQUAL, Literal(False))) is False
    assert interpreter.evaluate(Binary(Literal(None), NOT_EQUAL, Literal(False))) is True
    assert interpreter.evaluate(Binary(Literal(12), NOT_EQUAL, Literal("12"))) is True
    assert interpreter.evaluate(Binary(Literal(12), NOT_EQUAL, Binary(Literal(4), MULTIPLY, Literal(3)))) is False


def test_is_truthy(interpreter):
    assert interpreter.is_truthy(True) is True
    assert interpreter.is_truthy(False) is False
    assert interpreter.is_truthy(None) is False
    assert interpreter.is_truthy(666) is True
    assert interpreter.is_truthy(0) is True
    assert interpreter.is_truthy("so true") is True
    assert interpreter.is_truthy("") is True


def test_runtime_errors(interpreter):
    with pytest.raises(LoxRuntimeError) as ex:
        interpreter.evaluate(Unary(MINUS, Literal("fail")))
        assert False  # we should never arrive here
    assert ex.value.args == (MINUS, "fail", "Operand must be a number.")