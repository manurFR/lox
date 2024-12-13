import pytest

from scanning import Token
from syntax import Block, Print, Expression, Binary, Literal, Var, Variable # type: ignore
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


def test_execute_variable_declaration(interpreter, capsys):
    a = Token("IDENTIFIER", "a", None, 1)
    interpreter.execute(Var(a, Literal(3.14)))
    interpreter.execute(Print(Variable(a)))
    assert capsys.readouterr()[0] == "3.14\n"


def test_execute_statements_in_block(interpreter, capsys):
    a = Token("IDENTIFIER", "a", None, 1)
    interpreter.execute(Block([
        Var(a, Literal(3.14)),
        Print(Variable(a))
    ]))
    assert capsys.readouterr()[0] == "3.14\n"
