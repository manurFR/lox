"""
Nodes and leaves for the Abstract Syntax Tree (AST)

Display the tree by calling repr(root) or print(root)
"""

from dataclasses import dataclass
from typing import Any


class NodeExpr:
    # Only for type hints
    pass


@dataclass
class Binary(NodeExpr):
    left: NodeExpr  # expr
    operator: str
    right: NodeExpr  # expr

    def __repr__(self) -> str:
        return f"({self.operator} {self.left} {self.right})"


@dataclass
class Unary(NodeExpr):
    operator: str
    right: NodeExpr  # expr

    def __repr__(self) -> str:
        return f"({self.operator} {self.right})"


@dataclass
class Literal(NodeExpr):
    value: Any

    def __repr__(self) -> str:
        if self.value is None:
            return "nil"
        return str(self.value).lower()
    

@dataclass
class Grouping(NodeExpr):
    expr: NodeExpr

    def __repr__(self) -> str:
        return f"(group {self.expr})"
