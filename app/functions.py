from abc import ABC, abstractmethod
import time
from typing import Any

from environment import Environment


class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        """Number of arguments required"""
        pass
    
    @abstractmethod
    def call(self, interpreter: 'Interpreter', arguments: list[Any]) -> Any: # type: ignore
        pass


def register_native_functions(global_environment: Environment):
    global_environment.define("clock", NativeClock())


class NativeClock(LoxCallable):
    def arity(self) -> int:
        return 0
    
    def call(self, interpreter: 'Interpreter', arguments: list[Any]) -> float: # type: ignore
        return time.time()