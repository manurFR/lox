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
    """Actually, this represents functions AND class methods."""
    def __init__(self, declaration: Function, closure: Environment) -> None:
        self.declaration = declaration
        self.closure = closure

    def arity(self) -> int:
        return len(self.declaration.params)
    
    def call(self, interpreter, arguments: list[Any]) -> Any:
        environment = Environment(enclosing=self.closure)
        for param, value in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, value)

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as retex:
            return retex.value
        
    def bind(self, instance: 'LoxInstance'):  # type: ignore
        """For class methods only. When a method is referenced, return it but as a copy 
           where 'this' is bound to the instance from which it was called."""
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxUserFunction(self.declaration, environment)

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
    

class BreakException(Exception):
    pass


class ReturnException(RuntimeError):
    def __init__(self, value: Any) -> None:
        self.value = value