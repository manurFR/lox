import pytest
from errors import LoxRuntimeError
from evaluating import Interpreter  # type: ignore
from scanning import Token
from syntax import Assign, Literal, Grouping, Logical, Unary, Binary, Var, Variable  # type: ignore
from tokens import AND, DIVISE, EQUAL_EQUAL, GREATER, GREATER_EQUAL, LESS, LESS_EQUAL, MINUS, MULTIPLY, NOT, NOT_EQUAL, OR, PLUS

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
    assert interpreter.evaluate(Binary(Literal(10.0), MULTIPLY, Literal(2.5))) == 25
    assert interpreter.evaluate(Binary(Literal(10.0), DIVISE, Literal(4.0))) == 2.5
    # 6 * 2.5 / (2 * 3) => (/ (* 6.0 2.5) (group (* 2.0 3.0)))
    assert interpreter.evaluate(
        Binary(Binary(Literal(6.0), MULTIPLY, Literal(2.5)), DIVISE, Grouping(Binary(Literal(2.0), MULTIPLY, Literal(3.0))))) == 2.5

    assert interpreter.evaluate(Binary(Literal(12.8), MINUS, Literal(4.3))) == 8.5
    assert interpreter.evaluate(Binary(Literal(12.8), PLUS, Literal(4.3))) == 17.1
    # 6 + 4 * 3 == 18 => (+ 6.0 (* 4.0 3.0))
    assert interpreter.evaluate(Binary(Literal(6.0), PLUS, Binary(Literal(4.0), MULTIPLY, Literal(3.0)))) == 18
    # (6 + 4) * 3 == 30 => (* (group (+ 6.0 4.0)) 3.0)
    assert interpreter.evaluate(Binary(Grouping(Binary(Literal(6.0), PLUS, Literal(4.0))), MULTIPLY, Literal(3.0))) == 30


def test_evaluate_string_concatenation(interpreter):
    assert interpreter.evaluate(Binary(Literal("post"), PLUS, Literal("rock"))) == "postrock"


def test_evalute_comparison_operators(interpreter):
    assert interpreter.evaluate(Binary(Literal(12.3), GREATER, Literal(3.14))) is True
    assert interpreter.evaluate(Binary(Literal(12.3), LESS_EQUAL, Literal(3.14))) is False
    assert interpreter.evaluate(Binary(Literal(12.3), LESS_EQUAL, Literal(12.30))) is True
    assert interpreter.evaluate(Binary(Literal(12.3), GREATER_EQUAL, Literal(12.30))) is True
    assert interpreter.evaluate(Binary(Literal(12.3), GREATER_EQUAL, Literal(0.0))) is True
    assert interpreter.evaluate(Binary(Literal(-8.1), LESS, Literal(0.0))) is True


def test_evaluate_equality_operators(interpreter):
    assert interpreter.evaluate(Binary(Literal(12.0), EQUAL_EQUAL, Literal(12.0))) is True
    assert interpreter.evaluate(Binary(Literal("test"), EQUAL_EQUAL, Literal("test"))) is True
    assert interpreter.evaluate(Binary(Literal(True), EQUAL_EQUAL, Literal(False))) is False
    assert interpreter.evaluate(Binary(Literal(None), NOT_EQUAL, Literal(False))) is True
    assert interpreter.evaluate(Binary(Literal(12.0), NOT_EQUAL, Literal("12"))) is True
    assert interpreter.evaluate(Binary(Literal(12.0), NOT_EQUAL, Binary(Literal(4.0), MULTIPLY, Literal(3.0)))) is False


def test_evaluate_logical_operators(interpreter):
    assert interpreter.evaluate(Logical(Literal(True), OR, Literal(12.3))) == True
    assert interpreter.evaluate(Logical(Literal(False), OR, Literal(12.3))) == 12.3
    assert interpreter.evaluate(Logical(Literal(True), AND, Literal(12.3))) == 12.3
    assert interpreter.evaluate(Logical(Literal(False), AND, Literal(12.3))) == False
    assert interpreter.evaluate(Logical(Literal(True), AND, Literal(None))) is None


def test_evaluate_variable_reading(interpreter):
    interpreter.environment.define("a", 12.3)  # the variable must be defined before we can read it value
    assert interpreter.evaluate(Variable(Token("IDENTIFIER", "a", None, 1))) == 12.3


def test_evaluate_assignment(interpreter):
    interpreter.environment.define("v", None)  # "v" must be defined before we can assign it a value
    assert interpreter.evaluate(Assign(Token("IDENTIFIER", "v", None, 1), Literal("test"))) == "test"
    assert "v" in interpreter.environment.values
    assert interpreter.environment.values["v"] == "test"


def test_is_truthy(interpreter):
    assert interpreter.is_truthy(True) is True
    assert interpreter.is_truthy(False) is False
    assert interpreter.is_truthy(None) is False
    assert interpreter.is_truthy(666.0) is True
    assert interpreter.is_truthy(0) is True
    assert interpreter.is_truthy("so true") is True
    assert interpreter.is_truthy("") is True


def test_runtime_errors(interpreter):
    with pytest.raises(LoxRuntimeError) as ex:
        interpreter.evaluate(Unary(MINUS, Literal("fail")))
    assert ex.value.args == (MINUS, "Operand must be a number.")

    with pytest.raises(LoxRuntimeError) as ex:
        interpreter.evaluate(Binary(Literal(True), MULTIPLY, Literal(28.0)))
    with pytest.raises(LoxRuntimeError) as ex:
        interpreter.evaluate(Binary(Literal(5.0), DIVISE, Literal("3")))
    with pytest.raises(LoxRuntimeError) as ex:
        interpreter.evaluate(Binary(Literal(5.0), MINUS, Literal(None)))
    with pytest.raises(LoxRuntimeError) as ex:
        interpreter.evaluate(Binary(Literal(56.0), PLUS, Literal("quatre")))
    with pytest.raises(LoxRuntimeError) as ex:
        interpreter.evaluate(Binary(Literal(56.0), GREATER, Literal("quatre")))
    with pytest.raises(LoxRuntimeError) as ex:
        interpreter.evaluate(Binary(Literal(False), GREATER_EQUAL, Literal("quatre")))
    with pytest.raises(LoxRuntimeError) as ex:
        interpreter.evaluate(Binary(Literal("foo"), LESS, Literal(99.9)))
    with pytest.raises(LoxRuntimeError) as ex:
        interpreter.evaluate(Binary(Literal("vier"), LESS_EQUAL, Literal("funf")))
