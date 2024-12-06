import pytest
from environment import Environment
from errors import LoxRuntimeError
from scanning import Token


def test_Environmnent_define():
    e = Environment()
    e.define("v1", 12.3)
    e.define("v2", "hello")
    assert e.values == {"v1": 12.3, "v2": "hello"}
    e.define("v1", 66.6)
    assert e.values == {"v1": 66.6, "v2": "hello"}


def test_Environment_get():
    e = Environment()
    e.define("v1", 44.4)
    assert e.get(Token("IDENTIFIER", "v1", None, 3)) == 44.4
    with pytest.raises(LoxRuntimeError) as exc:
        e.get(Token("IDENTIFIER", "zzz", None, 4))
    assert exc.value.args == (Token("IDENTIFIER", "zzz", None, 4), "Undefined variable 'zzz'.")
