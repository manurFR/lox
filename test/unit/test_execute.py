import pytest

from syntax import Print, Expression, Binary, Literal # type: ignore
from evaluating import Interpreter # type: ignore
from tokens import PLUS


@pytest.fixture
def interpreter():
    return Interpreter()


def test_execute_print(interpreter, capsys):
    interpreter.execute(Print(Binary(Literal(2.2), PLUS, Literal(3.3))))
    assert capsys.readouterr()[0] == "5.5\n"


def test_execute_expression_statement(interpreter, capsys):
    interpreter.execute(Expression(Binary(Literal(2.2), PLUS, Literal(3.3))))
    assert capsys.readouterr()[0] == ""
