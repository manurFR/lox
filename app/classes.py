from typing import Any
from functions import LoxCallable


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

    def __repr__(self) -> str:
        return f"<instanceof {self.klass.name}>"
