from dataclasses import dataclass
from typing import Any


@dataclass
class Binary:
    left: Any  # expr
    operator: str
    right: Any  # expr

    def __repr__(self) -> str:
        return f"({self.operator} {self.left} {self.right})"


@dataclass
class Unary:
    operator: str
    right: Any  # expr

    def __repr__(self) -> str:
        return f"({self.operator} {self.right})"


@dataclass
class Literal:
    value: Any

    def __repr__(self) -> str:
        if self.value is None:
            return "nil"
        return str(self.value).lower()
    

@dataclass
class Grouping:
    expr: Any

    def __repr__(self) -> str:
        return f"(group {self.expr})"
