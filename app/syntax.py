"""
Nodes and leaves for the Abstract Syntax Tree (AST)

Display the tree by calling repr(root) or print(root)
"""

from dataclasses import dataclass
from typing import Any, Optional

# Nodes for Expression statements (frozen in order to be hashable, and thus valid dict keys in Interpreter._locals)

class NodeExpr:
    # Only for type hints
    pass


@dataclass(frozen=True)
class Binary(NodeExpr):
    left: NodeExpr  # expr
    operator: 'Token'  # type: ignore
    right: NodeExpr  # expr

    def __repr__(self) -> str:
        return f"({self.operator.lexeme} {self.left} {self.right})"


@dataclass(frozen=True)
class Unary(NodeExpr):
    operator: 'Token'  # type: ignore
    right: NodeExpr  # expr

    def __repr__(self) -> str:
        return f"({self.operator.lexeme} {self.right})"


@dataclass(frozen=True)
class Literal(NodeExpr):
    value: Any

    def __repr__(self) -> str:
        if self.value is None:
            return "nil"
        return str(self.value).lower()
    

@dataclass(frozen=True)
class Logical(NodeExpr):
    left: NodeExpr
    operator: 'Token'  # type: ignore
    right: NodeExpr

    def __repr__(self) -> str:
        return f"{self.left} {self.operator.lexeme} {self.right}"
    

@dataclass(frozen=True)
class Grouping(NodeExpr):
    expr: NodeExpr

    def __repr__(self) -> str:
        return f"(group {self.expr})"
    

@dataclass(frozen=True)
class Variable(NodeExpr):
    """Expression for getting a variable value"""
    name: 'Token' # type: ignore

    def __repr__(self) -> str:
        return self.name.lexeme


@dataclass(frozen=True)
class Assign(NodeExpr):
    name: 'Token' # type: ignore
    value: NodeExpr

    def __repr__(self) -> str:
        return f"{self.name.lexeme} = {self.value}"
    

@dataclass(frozen=True)
class Call(NodeExpr):
    callee: NodeExpr  # the left expression that evaluates to the function to call
    paren: 'Token'  # type: ignore  # the token for the opening parenthese, for error reporting
    arguments: list[NodeExpr]

    def __repr__(self) -> str:
        return f"{self.callee}({', '.join(repr(arg) for arg in self.arguments)})"
    

@dataclass(frozen=True)
class Get(NodeExpr):
    """ Fetching a value from an instance with instance.property is the 'Get' expression """
    instance: NodeExpr
    name: 'Token'  # type: ignore  # the property

    def __repr__(self) -> str:
        return f"{repr(self.instance)}.{self.name.lexeme}"
    

@dataclass(frozen=True)
class Set(NodeExpr):
    """ Setting an instance property with instance.property = <value> is the 'Set' expression """
    instance: NodeExpr
    name: 'Token'  # type: ignore  # the property
    value: NodeExpr

    def __repr__(self) -> str:
        return f"{repr(self.instance)}.{self.name.lexeme} = {repr(self.value)}"
    

@dataclass(frozen=True)
class This(NodeExpr):
    token: 'Token'  # type: ignore

    def __repr__(self) -> str:
        return self.token.lexeme


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
    initializer: Optional[NodeExpr]

    def __repr__(self) -> str:
        return f"var {self.name.lexeme}{" = " + repr(self.initializer) if self.initializer else ''};"


@dataclass
class While(NodeStmt):
    condition: NodeExpr
    body: NodeStmt
    increment: Optional[NodeExpr]  # must be kept here for 'continue' to work in 'for' statements with increment

    def __repr__(self) -> str:
        return f"while ({self.condition}) {self.body}"
    

@dataclass
class AbortLoop(NodeStmt):
    token: 'Token' # type: ignore

    def __repr__(self) -> str:
        return f"{self.token.lexeme};"
        

@dataclass
class Block(NodeStmt):
    statements: list[NodeStmt]

    def __repr__(self) -> str:
        return "{" + "\n".join(repr(stmt) for stmt in self.statements) + "}"
    

@dataclass
class Function(NodeStmt):
    name: 'Token'  # type: ignore
    params: 'list[Token]'  # type: ignore
    body: list[NodeStmt]

    def __repr__(self) -> str:
        return f"fun {self.name.lexeme}({', '.join(p.lexeme for p in self.params)}) {{ {repr(self.body)} }}"
    

@dataclass
class Return(NodeStmt):
    token: 'Token'  # type: ignore
    value: Optional[NodeExpr]

    def __repr__(self) -> str:
        return f"return{f' {repr(self.value)}' if self.value else ''};"
    

@dataclass
class Class(NodeStmt):
    name: 'Token'  # type: ignore
    methods: list[Function]

    def __repr__(self) -> str:
        return f"class {self.name.lexeme} {{ {self.methods} }}"
