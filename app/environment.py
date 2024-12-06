from typing import Any

from errors import LoxRuntimeError
from scanning import Token


class Environment:
    """The Environment holds the variables and their values"""
    def __init__(self) -> None:
        self.values = {}

    def define(self, name: str, value: Any) -> None:
        """A variable can be re-defined any number of times"""
        self.values[name] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
