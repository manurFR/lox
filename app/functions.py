from abc import ABC, abstractmethod
import time
from typing import Any

from environment import Environment
from syntax import Function


class LoxCallable(ABC):
    """Abstract Base Class => all @abstractmethod definitions MUST be implemented by subclasses"""
    @abstractmethod
    def arity(self) -> int:
        """Number of arguments required"""
        pass
    
    @abstractmethod
    def call(self, interpreter, arguments: list[Any]) -> Any: 
        pass


class LoxUserFunction(LoxCallable):
    def __init__(self, declaration: Function) -> None:
        self.declaration = declaration

    def arity(self) -> int:
        return len(self.declaration.params)
    
    def call(self, interpreter, arguments: list[Any]) -> Any:
        environment = Environment(enclosing=interpreter.globals)
        for param, value in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, value)
        interpreter.execute_block(self.declaration.body, environment)

    def __repr__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"
        

def register_native_functions(global_environment: Environment):
    global_environment.define("clock", _NativeClock())


class _NativeClock(LoxCallable):
    def arity(self) -> int:
        return 0
    
    def call(self, interpreter, arguments: list[Any]) -> float:
        return time.time()
    
    def __repr__(self) -> str:
        return f"<fn clock (native)>"