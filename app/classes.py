from typing import Any, Optional
from errors import LoxRuntimeError
from functions import LoxCallable, LoxUserFunction
from scanning import Token


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: dict[str, LoxUserFunction]) -> None:
        self.name = name
        self.methods = methods

    def __repr__(self) -> str:
        return f"<class {self.name}>"
    
    def call(self, interpreter, arguments: list[Any]) -> Any: 
        return LoxInstance(self)

    def arity(self) -> int:
        return 0  # TODO constructor arguments
    
    def find_method(self, name: str) -> Optional[LoxUserFunction]:
        return self.methods.get(name)  # None if no method by that name
    

class LoxInstance:
    def __init__(self, klass) -> None:
        self.klass = klass
        self.fields = {}

    def get(self, name: Token) -> Any:
        if name.lexeme in self.fields:  # property
            return self.fields[name.lexeme]
        elif method := self.klass.find_method(name.lexeme):  # method
            return method
        else:
            raise LoxRuntimeError(name, f"Undefined property '{name.lexeme}'.")
        
    def set_value(self, name: Token, value: Any):
        self.fields[name.lexeme] = value

    def __repr__(self) -> str:
        return f"<instanceof {self.klass.name}>"
