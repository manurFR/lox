"""
Nodes and leaves for the Abstract Syntax Tree (AST)

Display the tree by calling repr(root) or print(root)
"""

from dataclasses import dataclass
from typing import Any, Optional

# Nodes for Expression statements (frozen in order to be hashable, and thus valid dict keys in Interpreter._locals)

class NodeExpr:
    # Only for type hints
    def print_ast(self, level=0):
        pass  # override this


@dataclass(frozen=True)
class Binary(NodeExpr):
    left: NodeExpr  # expr
    operator: 'Token'  # type: ignore
    right: NodeExpr  # expr

    def __repr__(self) -> str:
        return f"({self.operator.lexeme} {self.left} {self.right})"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Expr] Binary: {self.operator.lexeme}")
        self.left.print_ast(level + 1)
        self.right.print_ast(level + 1)


@dataclass(frozen=True)
class Unary(NodeExpr):
    operator: 'Token'  # type: ignore
    right: NodeExpr  # expr

    def __repr__(self) -> str:
        return f"({self.operator.lexeme} {self.right})"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Expr] Unary: {self.operator.lexeme}")
        self.right.print_ast(level + 1)


@dataclass(frozen=True)
class Literal(NodeExpr):
    value: Any

    def __repr__(self) -> str:
        if self.value is None:
            return "nil"
        return str(self.value).lower()
    
    def print_ast(self, level=0):
        _print_level(level, f"[Expr] Literal: {self.value}")
    

@dataclass(frozen=True)
class Logical(NodeExpr):
    left: NodeExpr
    operator: 'Token'  # type: ignore
    right: NodeExpr

    def __repr__(self) -> str:
        return f"{self.left} {self.operator.lexeme} {self.right}"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Expr] Logical: {self.operator.lexeme}")
        self.left.print_ast(level + 1)
        self.right.print_ast(level + 1)
    

@dataclass(frozen=True)
class Grouping(NodeExpr):
    expr: NodeExpr

    def __repr__(self) -> str:
        return f"(group {self.expr})"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Expr] Grouping:")
        self.expr.print_ast(level + 1)
    

@dataclass(frozen=True)
class Variable(NodeExpr):
    """Expression for getting a variable value"""
    name: 'Token' # type: ignore

    def __repr__(self) -> str:
        return self.name.lexeme
    
    def print_ast(self, level=0):
        _print_level(level, f"[Expr] Variable (getting): {self.name.lexeme}")


@dataclass(frozen=True)
class Assign(NodeExpr):
    name: 'Token' # type: ignore
    value: NodeExpr

    def __repr__(self) -> str:
        return f"{self.name.lexeme} = {self.value}"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Expr] Assign (variable): {self.name.lexeme}")
        self.value.print_ast(level + 1)
    

@dataclass(frozen=True)
class Call(NodeExpr):
    callee: NodeExpr  # the left expression that evaluates to the function to call
    paren: 'Token'  # type: ignore  # the token for the opening parenthese, for error reporting
    arguments: tuple[NodeExpr]

    def __repr__(self) -> str:
        return f"{self.callee}({', '.join(repr(arg) for arg in self.arguments)})"
    
    def print_ast(self, level=0):
        _print_level(level, "[Expr] Call...")
        self.callee.print_ast(level + 1)
        _print_level(level, f"...with {len(self.arguments)} arguments{':' if self.arguments else ''}")
        for idx_arg, arg in enumerate(self.arguments):
            arg.print_ast(level + 1)
            if idx_arg < len(self.arguments) - 1:
                _print_level(level + 1, ", -----")
    

@dataclass(frozen=True)
class Get(NodeExpr):
    """ Fetching a value from an instance with instance.property is the 'Get' expression """
    instance: NodeExpr
    name: 'Token'  # type: ignore  # the property

    def __repr__(self) -> str:
        return f"{repr(self.instance)}.{self.name.lexeme}"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Expr] Get (property) {self.name.lexeme} from:")
        self.instance.print_ast(level + 1)
    

@dataclass(frozen=True)
class Set(NodeExpr):
    """ Setting an instance property with instance.property = <value> is the 'Set' expression """
    instance: NodeExpr
    name: 'Token'  # type: ignore  # the property
    value: NodeExpr

    def __repr__(self) -> str:
        return f"{repr(self.instance)}.{self.name.lexeme} = {repr(self.value)}"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Expr] Set (property) {self.name.lexeme} from:")
        self.instance.print_ast(level + 1)
        _print_level(level, "...with value:")
        self.value.print_ast(level + 1)
        

@dataclass(frozen=True)
class Super(NodeExpr):
    token: 'Token'  # type: ignore
    method: 'Token'  # type: ignore
    
    def __repr__(self) -> str:
        return f"super.{self.method.lexeme}"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Expr] Super, calling method {self.method.lexeme}() from superclass")
    

@dataclass(frozen=True)
class This(NodeExpr):
    token: 'Token'  # type: ignore

    def __repr__(self) -> str:
        return self.token.lexeme

    def print_ast(self, level=0):
        _print_level(level, f"[Expr] This")

# Nodes for other statements

class NodeStmt:
    # Only for type hints
    def print_ast(self, level=0):
        pass  # override this


@dataclass
class Expression(NodeStmt):
    expr: NodeExpr

    def __repr__(self) -> str:
        return repr(self.expr)
    
    def print_ast(self, level=0):
        _print_level(level, f"[Stmt] Expression")
        self.expr.print_ast(level + 1)
        

@dataclass
class If(NodeStmt):
    condition: NodeExpr
    then_stmt: NodeStmt
    else_stmt: Optional[NodeStmt]

    def __repr__(self) -> str:
        return (f"if ({self.condition}) then {repr(self.then_stmt)}" +
                (f" else {self.else_stmt}" if self.else_stmt is not None else ""))
    

    def print_ast(self, level=0):
        _print_level(level, f"[Stmt] If...")
        self.condition.print_ast(level + 1)
        _print_level(level, f"[Stmt] ...Then...")
        self.then_stmt.print_ast(level + 1)
        if self.else_stmt:
            _print_level(level, f"[Stmt] ...Else...")
            self.else_stmt.print_ast(level + 1)
    

@dataclass
class Print(NodeStmt):
    expr: NodeExpr

    def __repr__(self) -> str:
        return f"print {self.expr};"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Stmt] Print")
        self.expr.print_ast(level + 1)


@dataclass 
class Var(NodeStmt):
    """Statement for declaring a variable (with optional setting)"""
    name: 'Token' # type: ignore
    initializer: Optional[NodeExpr]

    def __repr__(self) -> str:
        return f"var {self.name.lexeme}{" = " + repr(self.initializer) if self.initializer else ''};"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Stmt] Var (declaration): {self.name.lexeme}")
        if self.initializer:
            _print_level(level, "...with initialization:")
            self.initializer.print_ast(level + 1)


@dataclass
class While(NodeStmt):
    condition: NodeExpr
    body: NodeStmt
    increment: Optional[NodeExpr]  # must be kept here for 'continue' to work in 'for' statements with increment

    def __repr__(self) -> str:
        return f"while ({self.condition}) {self.body}"

    def print_ast(self, level=0):
        _print_level(level, f"[Stmt] While...")
        self.condition.print_ast(level + 1)
        _print_level(level, "...Do...")
        self.body.print_ast(level + 1)
        if self.increment:
            self.increment.print_ast(level + 1)


@dataclass
class AbortLoop(NodeStmt):
    token: 'Token' # type: ignore

    def __repr__(self) -> str:
        return f"{self.token.lexeme};"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Stmt] AbortLoop: {self.token.lexeme}")
        

@dataclass
class Block(NodeStmt):
    statements: list[NodeStmt]

    def __repr__(self) -> str:
        return "{" + "\n".join(repr(stmt) for stmt in self.statements) + "}"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Stmt] Block")
        for stmt in self.statements:
            stmt.print_ast(level + 1)
    

@dataclass
class Function(NodeStmt):
    name: 'Token'  # type: ignore
    params: 'list[Token]'  # type: ignore
    body: list[NodeStmt]

    def __repr__(self) -> str:
        return f"fun {self.name.lexeme}({', '.join(p.lexeme for p in self.params)}) {{ {repr(self.body)} }}"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Stmt] Function (declaration): {self.name.lexeme}...")
        _print_level(level, f"...with params ({', '.join(p.lexeme for p in self.params)}):")
        for stmt in self.body:
            stmt.print_ast(level + 1)
    

@dataclass
class Return(NodeStmt):
    token: 'Token'  # type: ignore
    value: Optional[NodeExpr]

    def __repr__(self) -> str:
        return f"return{f' {repr(self.value)}' if self.value else ''};"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Stmt] Return{' value:' if self.value else ''}")
        if self.value:
            self.value.print_ast(level + 1)
    

@dataclass
class Class(NodeStmt):
    name: 'Token'  # type: ignore
    superclass: Optional[Variable]
    methods: list[Function]

    def __repr__(self) -> str:
        return f"class {self.name.lexeme}{f' < {self.superclass}' if self.superclass else ''} {{ {self.methods} }}"
    
    def print_ast(self, level=0):
        _print_level(level, f"[Stmt] Class (declaration): {self.name.lexeme}")
        if self.superclass:
            _print_level(level, f"... inheriting from superclass {self.superclass}")
        _print_level(level, f"{'... with methods:' if self.methods else ''}")
        for method in self.methods:
            method.print_ast(level + 1)


# --

def _print_level(level, node):
    print(f"{' '*level*2}{node}")