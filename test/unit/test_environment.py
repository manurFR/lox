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


def test_Environment_get_from_enclosing_or_shadowed():
    parent = Environment()
    parent.define("v1", 44.4)
    parent.define("v2", 100)
    blockscope = Environment(enclosing=parent)
    blockscope.define("v1", 11.1)
    assert blockscope.get(Token("IDENTIFIER", "v1", None, 3)) == 11.1
    assert blockscope.get(Token("IDENTIFIER", "v2", None, 3)) == 100
    with pytest.raises(LoxRuntimeError) as exc:
        blockscope.get(Token("IDENTIFIER", "zzz", None, 4))
    assert exc.value.args == (Token("IDENTIFIER", "zzz", None, 4), "Undefined variable 'zzz'.")


def test_Environment_assign():
    e = Environment()
    e.define("v", None)
    var_token = Token("IDENTIFIER", "v", None, 1)
    assert e.get(var_token) is None
    e.assign(var_token, 99.9)
    assert e.get(var_token) == 99.9

    with pytest.raises(LoxRuntimeError) as exc:
        e.assign(Token("IDENTIFIER", "zzz", None, 4), "hello")
    assert exc.value.args == (Token("IDENTIFIER", "zzz", None, 4), "Undefined variable 'zzz'.")


def test_Environment_assign_to_enclosing_or_shadowed():
    parent = Environment()
    parent.define("v1", 44.4)
    v1_token = Token("IDENTIFIER", "v1", None, 1)
    blockscope = Environment(enclosing=parent)
    blockscope.define("v2", 100)
    v2_token = Token("IDENTIFIER", "v2", None, 1)
    blockscope.assign(v1_token, 11.1)
    blockscope.assign(v2_token, 200)

    assert blockscope.get(v1_token) == 11.1
    assert blockscope.get(v2_token) == 200
    assert parent.get(v1_token) == 11.1

    with pytest.raises(LoxRuntimeError) as exc:
        parent.assign(v2_token, "hello")
    assert exc.value.args == (v2_token, "Undefined variable 'v2'.")
