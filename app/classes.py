from typing import Any, Optional
from errors import LoxRuntimeError
from functions import LoxCallable, LoxUserFunction
from scanning import Token


class LoxClass(LoxCallable):
    def __init__(self, name: str, superclass: Optional['LoxClass'], methods: dict[str, LoxUserFunction]) -> None:
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def __repr__(self) -> str:
        return f"<class {self.name}>"
    
    def call(self, interpreter, arguments: list[Any]) -> Any:
        """Creating an instance of the class.
           Call the init() method immediately if it exists."""
        instance = LoxInstance(self)
        if initializer := self.find_method("init"):
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def arity(self) -> int:
        if initializer := self.find_method("init"):
            return initializer.arity()
        else:
            return 0
    
    def find_method(self, name: str) -> Optional[LoxUserFunction]:
        if name in self.methods:
            return self.methods[name]
        if self.superclass:
            return self.superclass.find_method(name)
        return None  # if no method found by that name
    

class LoxInstance:
    def __init__(self, klass) -> None:
        self.klass = klass
        self.fields = {}

    def get(self, name: Token) -> Any:
        if name.lexeme in self.fields:  # property
            return self.fields[name.lexeme]
        elif method := self.klass.find_method(name.lexeme):  # method
            return method.bind(self)
        else:
            raise LoxRuntimeError(name, f"Undefined property '{name.lexeme}'.")
        
    def set_value(self, name: Token, value: Any):
        self.fields[name.lexeme] = value

    def __repr__(self) -> str:
        return f"<instanceof {self.klass.name}>"
