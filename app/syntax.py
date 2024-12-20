"""
Nodes and leaves for the Abstract Syntax Tree (AST)

Display the tree by calling repr(root) or print(root)
"""

from dataclasses import dataclass
from typing import Any, Optional

# Nodes for Expression statements

class NodeExpr:
    # Only for type hints
    pass


@dataclass
class Binary(NodeExpr):
    left: NodeExpr  # expr
    operator: 'Token'  # type: ignore
    right: NodeExpr  # expr

    def __repr__(self) -> str:
        return f"({self.operator.lexeme} {self.left} {self.right})"


@dataclass
class Unary(NodeExpr):
    operator: 'Token'  # type: ignore
    right: NodeExpr  # expr

    def __repr__(self) -> str:
        return f"({self.operator.lexeme} {self.right})"


@dataclass
class Literal(NodeExpr):
    value: Any

    def __repr__(self) -> str:
        if self.value is None:
            return "nil"
        return str(self.value).lower()
    

@dataclass
class Logical(NodeExpr):
    left: NodeExpr
    operator: 'Token'  # type: ignore
    right: NodeExpr

    def __repr__(self) -> str:
        return f"{self.left} {self.operator.lexeme} {self.right}"
    

@dataclass
class Grouping(NodeExpr):
    expr: NodeExpr

    def __repr__(self) -> str:
        return f"(group {self.expr})"
    

@dataclass
class Variable(NodeExpr):
    """Expression for getting a variable value"""
    name: 'Token' # type: ignore

    def __repr__(self) -> str:
        return self.name.lexeme


@dataclass
class Assign(NodeExpr):
    name: 'Token' # type: ignore
    value: NodeExpr

    def __repr__(self) -> str:
        return f"{self.name.lexeme} = {self.value}"


# Nodes for other statements

class NodeStmt:
    # Only for type hints
    pass


@dataclass
class Expression(NodeStmt):
    expr: NodeExpr

    def __repr__(self) -> str:
        return repr(self.expr)
    

@dataclass
class If(NodeStmt):
    condition: NodeExpr
    then_stmt: NodeStmt
    else_stmt: Optional[NodeStmt]

    def __repr__(self) -> str:
        return (f"if ({self.condition}) then {repr(self.then_stmt)}" +
                (f" else {self.else_stmt}" if self.else_stmt is not None else ""))
    

@dataclass
class Print(NodeStmt):
    expr: NodeExpr

    def __repr__(self) -> str:
        return f"print {self.expr};"


@dataclass 
class Var(NodeStmt):
    """Statement for declaring a variable (with optional setting)"""
    name: 'Token' # type: ignore
    expr: Optional[NodeExpr]

    def __repr__(self) -> str:
        return f"var {self.name.lexeme}{" = " + repr(self.expr) if self.expr else ''};"


@dataclass
class While(NodeStmt):
    condition: NodeExpr
    body: NodeStmt

    def __repr__(self) -> str:
        return f"while ({self.condition}) {self.body}"
        

@dataclass
class Block(NodeStmt):
    statements: list[NodeStmt]

    def __repr__(self) -> str:
        return "{" + "\n".join(repr(stmt) for stmt in self.statements) + "}"