
from collections import deque
from enum import Enum

from errors import Errors
from scanning import Token
from syntax import (AbortLoop, Assign, Binary, Block, Call, Class, Expression, Function, Get, Grouping, If, Literal, Logical, 
                    NodeExpr, NodeStmt, Print, Return, Set, Super, This, Unary, Var, Variable, While)


class FlowType(Enum):
    NONE = -1
    FUNCTION = 0
    METHOD = 1
    INITIALIZER = 2
    LOOP = 10

class ClassType(Enum):
    NONE = -1
    CLASS = 0
    SUBCLASS = 1


class Resolver:
    """This resolver does a static semantic analysis pass between parsing and evaluating steps.
       It will pre-evaluate each variable before the actual interpreting, and keep a reference 
       to the distance of the scope where the value of the variable is stored. "Distance" meaning
       the number of environments upwards it is present.
    """
    def __init__(self, interpreter) -> None:
        self.interpreter = interpreter
        self.scopes: deque[dict[str, bool]] = deque()  # Stack
        self.current_flow = FlowType.NONE  # to detect return statements at top level, break outside loops, etc.
        self.current_classtype = ClassType.NONE  # to detect 'this' outside of class methods 

    def resolve(self, node: NodeStmt) -> None:
        """Perform the semantic analysis and keep the record of the found variables.
           Walk the AST and for each variable found, record its distance from where it is kept in scope/environment."""
        match node:
            case Block() as block:
                self._begin_scope()
                self.resolve_statements(block.statements)
                self._end_scope()                

            case Var() as var_declaration:
                self._declare(var_declaration.name)
                if var_declaration.initializer:
                    self.resolve_expression(var_declaration.initializer)
                self._define(var_declaration.name)

            case Function() as function:
                # bind and record the function name
                self._declare(function.name)
                self._define(function.name)
                # bind the function's parameters to the inner function scope
                self.resolve_function(function, FlowType.FUNCTION)

            case Class() as stmt:
                enclosing_classtype = self.current_classtype
                self.current_classtype = ClassType.CLASS

                self._declare(stmt.name)
                self._define(stmt.name)
                
                if stmt.superclass:
                    if stmt.name.lexeme == stmt.superclass.name.lexeme:
                        self._error(stmt.superclass.name, "A class can't inherit from itself.")
                    self.current_classtype = ClassType.SUBCLASS
                    self.resolve_expression(stmt.superclass)
                    
                    self._begin_scope()  # for "super"
                    self._innerscope["super"] = True

                self._begin_scope()  # for "this" and the methods
                self._innerscope["this"] = True
                for method in stmt.methods:
                    if method.name.lexeme == "init":
                        declaration = FlowType.INITIALIZER
                    else:
                        declaration = FlowType.METHOD
                    self.resolve_function(method, declaration)
                self._end_scope()  # for "this" and the methods
                
                if stmt.superclass:
                    self._end_scope()  # for "super"

                self.current_classtype = enclosing_classtype

            case Expression() as stmt:
                self.resolve_expression(stmt.expr)

            case If() as stmt:
                """This is a sematic pass, so we resolve both branches then/else if they exists. We need to resolve all the code."""
                self.resolve_expression(stmt.condition)
                self.resolve(stmt.then_stmt)
                if stmt.else_stmt:
                    self.resolve(stmt.else_stmt)

            case Print() as stmt:
                self.resolve_expression(stmt.expr)

            case Return() as stmt:
                if self.current_flow == FlowType.NONE:
                    self._error(stmt.token, "Can't use 'return' in top-level code.")
                if stmt.value:
                    if self.current_flow == FlowType.INITIALIZER:
                        self._error(stmt.token, "Can't return a value from an initializer.")
                    self.resolve_expression(stmt.value)

            case While() as stmt:
                """This is a semantic pass, so we don't loop. We resolve each part once and only once."""
                enclosing_flow = self.current_flow
                self.current_flow = FlowType.LOOP
                self.resolve_expression(stmt.condition)
                if stmt.increment:
                    self.resolve_expression(stmt.increment)
                self.resolve(stmt.body)
                self.current_flow = enclosing_flow

            case AbortLoop() as stmt:
                if self.current_flow != FlowType.LOOP:
                    self._error(stmt.token, f"Can't use '{stmt.token.lexeme}' outside of loop.")

            case _:
                raise NotImplementedError(node)
            
    def resolve_statements(self, statements: list[NodeStmt]):
        for stmt in statements:
            self.resolve(stmt)

    def resolve_expression(self, node: NodeExpr):
        match node:
            case Variable() as variable:  # reading a variable
                if self._innerscope.get(variable.name.lexeme) is False:
                    self._error(variable.name, "Can't read local variable in its own initializer.")
                self.resolve_local(variable, variable.name)

            case Assign() as assign:  # setting the value of a variable
                self.resolve_expression(assign.value)
                self.resolve_local(assign, assign.name)

            case Binary() as binary:
                self.resolve_expression(binary.left)
                self.resolve_expression(binary.right)

            case Call() as call:
                 # the thing being called is an expression (that shoud evaluate to a function) so we need to resolve it
                 self.resolve_expression(call.callee)
                 for arg in call.arguments:
                     self.resolve_expression(arg)

            case Get() as get:
                self.resolve_expression(get.instance)

            case Set() as expr:
                self.resolve_expression(expr.instance)
                self.resolve_expression(expr.value)
                
            case Super() as expr:
                if self.current_classtype == ClassType.NONE:
                    self._error(expr.token, "Can't use 'super' outside of a class.")
                elif self.current_classtype == ClassType.CLASS:
                    self._error(expr.token, "Can't use 'super' in a class with no superclass.")
                self.resolve_local(expr, expr.token)

            case This() as this:
                if self.current_classtype == ClassType.NONE:
                    self._error(this.token, "Can't use 'this' outside of a class.")
                self.resolve_local(this, this.token)

            case Grouping() as grouping:
                self.resolve_expression(grouping.expr)

            case Literal() as literal:
                pass  # no variables or subexpression inside literals

            case Logical() as logical:
                """Semantic pass, so no short-circuitry, as we need to resolve each operand once."""
                self.resolve_expression(logical.left)
                self.resolve_expression(logical.right)

            case Unary() as unary:
                self.resolve_expression(unary.right)

            case _:
                raise NotImplementedError(node)
            
    def resolve_local(self, expr: NodeExpr, name: Token):
        for distance, scope in enumerate(reversed(self.scopes)):  # reverse walk the scopes, innermost to outermost
            if name.lexeme in scope:
                # Number of scopes between the current innermost scope and the one where the variable was found
                #  for example, if the variable was found in the current scope, distance == 1 ; if it's the
                #  immediately enclosing scope, distance == 1 ; etc.
                # If the variable is unresolved (ie. we never reach this 'if' block), we can assume it's global
                #  and thus not tracked in the resolver.
                self.interpreter.resolve(expr, distance)
                return

    def resolve_function(self, function: Function, functype: FlowType):
        enclosing_flow = self.current_flow
        self.current_flow = functype
        self._begin_scope()
        for param in function.params:
            self._declare(param)
            self._define(param)
        self.resolve_statements(function.body)
        self._end_scope()
        self.current_flow = enclosing_flow
    
    def _begin_scope(self):
        self.scopes.append(dict())

    def _end_scope(self):
        self.scopes.pop()

    def _declare(self, name: Token):
        if name.lexeme:
            if name.lexeme in self._innerscope:
                self._error(name, "A variable with the same name is already present in the same scope.")

            self._innerscope[name.lexeme] = False  # False mean "resolving not finished yet"

    def _define(self, name: Token):
        if name.lexeme:
            self._innerscope[name.lexeme] = True  # variable is ready

    @property
    def _innerscope(self) -> dict:
        if len(self.scopes) > 0:
            return self.scopes[-1]
        return {}
    
    def _error(self, token: Token, message: str):
        if token.toktype == "EOF":
            Errors.report(token.line, message, "at end")
        else:
            Errors.report(token.line, message, f" at '{token.lexeme}'")
        