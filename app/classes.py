from typing import Any
from errors import LoxRuntimeError
from functions import LoxCallable
from scanning import Token


class LoxClass(LoxCallable):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<class {self.name}>"
    
    def call(self, interpreter, arguments: list[Any]) -> Any: 
        return LoxInstance(self)

    def arity(self) -> int:
        return 0  # TODO constructor arguments
    

class LoxInstance:
    def __init__(self, klass) -> None:
        self.klass = klass
        self.fields = {}

    def get_value(self, name: Token) -> Any:
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        else:
            raise LoxRuntimeError(name, f"Undefined property '{name.lexeme}'.")
        
    def set_value(self, name: Token, value: Any):
        self.fields[name.lexeme] = value

    def __repr__(self) -> str:
        return f"<instanceof {self.klass.name}>"
