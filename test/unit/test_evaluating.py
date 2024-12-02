from evaluating import evaluate, is_truthy  # type: ignore
from syntax import Literal, Grouping, Unary, Binary  # type: ignore


def test_evaluate_literal_number():
    assert evaluate(Literal(12.345)) == 12.345
    assert evaluate(Literal(12.3450)) == 12.345
    assert evaluate(Literal(12.34506)) == 12.34506
    assert evaluate(Literal(12.0)) == 12
    assert evaluate(Literal(12)) == 12


def test_evaluate_literal_others():
    assert evaluate(Literal(True)) == True
    assert evaluate(Literal(False)) == False
    assert evaluate(Literal(None)) == None
    assert evaluate(Literal("python")) == "python"


def test_evaluate_grouping():
    assert evaluate(Grouping(Literal(None))) == None
    assert evaluate(Grouping(Literal(25.60))) == 25.6
    assert evaluate(Grouping(Grouping(Literal("so much parentheses!")))) == "so much parentheses!"


def test_evaluate_unary():
    assert evaluate(Unary("!", Literal(False))) == True
    assert evaluate(Unary("!", Literal(None))) == True
    assert evaluate(Unary("!", Literal(True))) == False
    assert evaluate(Unary("!", Literal(3.14))) == False
    assert evaluate(Unary("!", Literal("string"))) == False
    
    assert evaluate(Unary("-", Literal(3.14))) == -3.14
    assert evaluate(Unary("-", Grouping(Literal(12.0)))) == -12


def test_evaluate_arithmetic_operators():
    assert evaluate(Binary(Literal(10), "*", Literal(2.5))) == 25
    assert evaluate(Binary(Literal(10), "/", Literal(4))) == 2.5
    # 6 * 2.5 / (2 * 3) => (/ (* 6.0 2.5) (group (* 2.0 3.0)))
    assert evaluate(Binary(Binary(Literal(6), "*", Literal(2.5)), "/", Grouping(Binary(Literal(2), "*", Literal(3))))) == 2.5

    assert evaluate(Binary(Literal(12.8), "-", Literal(4.3))) == 8.5
    assert evaluate(Binary(Literal(12.8), "+", Literal(4.3))) == 17.1
    # 6 + 4 * 3 == 18 => (+ 6.0 (* 4.0 3.0))
    assert evaluate(Binary(Literal(6), "+", Binary(Literal(4), "*", Literal(3)))) == 18
    # (6 + 4) * 3 == 30 => (* (group (+ 6.0 4.0)) 3.0)
    assert evaluate(Binary(Grouping(Binary(Literal(6), "+", Literal(4))), "*", Literal(3))) == 30


def test_evaluate_string_concatenation():
    assert evaluate(Binary(Literal("post"), "+", Literal("rock"))) == "postrock"


def test_comparison_operators():
    assert evaluate(Binary(Literal(12.3), ">", Literal(3.14))) is True
    assert evaluate(Binary(Literal(12.3), "<=", Literal(3.14))) is False
    assert evaluate(Binary(Literal(12.3), "<=", Literal(12.30))) is True
    assert evaluate(Binary(Literal(12.3), ">=", Literal(12.30))) is True
    assert evaluate(Binary(Literal(12.3), ">=", Literal(0))) is True
    assert evaluate(Binary(Literal(-8), "<", Literal(0))) is True


def test_equality_operators():
    assert evaluate(Binary(Literal(12.0), "==", Literal(12))) is True
    assert evaluate(Binary(Literal("test"), "==", Literal("test"))) is True
    assert evaluate(Binary(Literal(True), "==", Literal(False))) is False
    assert evaluate(Binary(Literal(None), "!=", Literal(False))) is True
    assert evaluate(Binary(Literal(12), "!=", Literal("12"))) is True
    assert evaluate(Binary(Literal(12), "!=", Binary(Literal(4), "*", Literal(3)))) is False


def test_is_truthy():
    assert is_truthy(True) is True
    assert is_truthy(False) is False
    assert is_truthy(None) is False
    assert is_truthy(666) is True
    assert is_truthy(0) is True
    assert is_truthy("so true") is True
    assert is_truthy("") is True
