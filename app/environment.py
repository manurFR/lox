from typing import Any, Optional

from errors import LoxRuntimeError
from scanning import Token


class Environment:
    """The Environment holds the variables and their values"""
    def __init__(self, enclosing=None) -> None:
        self.values: dict[str, Any] = {}
        self.enclosing: Optional[Environment] = enclosing  # the "parent" environment for the enclosing scope

    def define(self, name: str, value: Any) -> None:
        """A variable can be re-defined any number of times"""
        self.values[name] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        # recursion up the chain of enclosing scope(s) to find (more) global variables        
        if self.enclosing:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
    
    def get_at(self, distance: int, name: str) -> Any:
        return self.ancestor(distance).values.get(name)

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        
        # if the variable was declared in an enclosing scope, push its assignment there
        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
    
    def assign_at(self, distance: int, name: Token, value: Any) -> None:
        if name.lexeme:
            self.ancestor(distance).values[name.lexeme] = value

    def ancestor(self, distance: int):
        environment = self
        for _ in range(distance):
            if environment.enclosing:
                environment = environment.enclosing
        return environment